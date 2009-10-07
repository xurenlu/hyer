#!/usr/bin/python
#coding:utf-8

STA_DONE=128
STA_ERR=1
#'''没有新任务时就休息2秒'''

import time
import threading
import copy
import MySQLdb
import hyer.log
import hyer.lock

class Worker(threading.Thread):
    '''
    Worker class 
    工人们从控制台取回下一步需要做的任务[原料],完成处理,再把原料交给控制台。
    工人们从控制台取任务时，有可能控制台返回说接下来没有任务需要完成。这时不能马上又去轮询，而是过n秒钟后再去询问,避免过度的空询问将Leader堵塞.
    每一个工人都需要知道:当前要完成的任务号,

    '''
    post="genericWorker"
    rest_time=0.2
    def init(self,post,tools,products,nextWorker,config={}):
        self.post=post
        self.tools=tools
        self.products=products
        self.nextWorker=nextWorker
        self.currentTool="null"
        self.config=config
        #for product in products:
        #    self.Leader.pushProduct(self.post,product)
        #pass

    def applyProducts(self,products):
        '''
        This method simply set the workers products to finish.
        as a rule,use this method to specific the first worker in the production line.
        这个方法直接设定当前worker所需要完成的产品
        一般情况下适用于某条流水线上最先开始干活的那个..
        ''' 
        self.products=products
    def addTools(self,tools):
        self.tools.extend(tools)
    def addTool(self,tool):
        self.tools.append(tool)
    def process(self,product):
        '''处理一件产品/加工一个作业'''
        for tool in self.tools:
            self.currentTool=tool
            try:
                product=tool["class"](tool).run(product)
            except hyer.error.IgnoreError,en:
                #error can be ignored
                hyer.log.debug("got error class:[%s] \nerror msg:%s \n worker:%s\ntool:[%s] " % ( str(en.__class__), en, self.post, self.currentTool))
                hyer.log.track()
                pass
            except hyer.error.ExitLoopError,ex:
                hyer.log.track()
                raise hyer.error.ExitLoopError(str(ex))
            except Exception,ec:
                hyer.log.info(  "got error class:[%s] \nerror msg:%s \n worker:%s\ntool:[%s] " % ( str(ec.__class__), ec, self.post, self.currentTool))
                hyer.log.track()
                #print product
                raise hyer.error.ExitLoopError( \
                        "got error:%s while tools process:%s,%s->[%s] " % ( str(ec.__class__), ec, self.post, self.currentTool)
                        )
                pass
        return product
    def report(self,status=STA_DONE):
        pass
    def mark_done(self,product_id):
        '''
        完成了一件产品,报告产品库解除锁定
        '''
        hyer.lock.lock("mark_done")
        try:
            hyer.production_db.ProductionDb(self.config).mark_done(product_id,self.post)
        except:
            pass
        hyer.lock.unLock()
    def run(self):
        '''
        '''
        if self.config.has_key("no_loop"):
            if self.config["no_loop"]:
                self.singleRun()
                return
        while True:
            try:
                self.singleRun()
            except Exception,e:
                hyer.log.trace()

    def singleRun(self):
        hyer.log.info("worker got new loop operation")
        try:
            product=self.fetchProduct(self.post)
            if product == None:
                time.sleep(self.rest_time)
                hyer.log.debug("worker got null product" )
            else:
                hyer.log.info("worker got new product")
                try:
                    product_id=product["__PRODUCT_ID__"]
                    output=self.process(product)
                    self.mark_done(product_id)
                except hyer.error.ExitLoopError,e1:
                    #print "got an ExitLoopError ",e1,":",self.post,":",self.currentTool
                    self.mark_done(product_id)
                    return None
                except Exception,e2:
                    hyer.log.error("error occured while processing tools %s" % str(e2))
                    return None 
                #如果这个流程至这儿结束了,就不用报告到控制台了..
                if self.nextWorker==None:
                    #hyer.log.error("nextWorker == None,exit") #这里是正常结束流程,不用报告.
                    return None 
                if isinstance(self.nextWorker,list):
                    for nw in self.nextWorker:
                        if isinstance(output,list):
                            for outproduct in output:
                                try:
                                    self.pushProduct(nw,outproduct)
                                except Exception,ep:
                                    hyer.log.error("pushProduct error:%s" % ep)
                        else:
                            try:
                                self.pushProduct(nw,output)
                            except Exception,ep:
                                hyer.log.error("pushProduct error:%s" % ep)
                else:
                   hyer.log.error("nextWorker must be a list .") 

        except Exception,e:
            hyer.log.error("fetchProduct() failed:%s" % e )
            time.sleep(self.rest_time)

    #从0.63开始,worker类自选向production_db存取产品.目的是,避免交叉引用,worker类不再和leader打交道.
    def pushProduct(self,nextWorker,product):
        '''
        将一份产品录入到库中.
        '''
        hyer.lock.lock("copy product")
        tempProduct=copy.copy(product)
        hyer.lock.unLock()
        hyer.lock.lock("pushProduct")
        try:
            hyer.production_db.ProductionDb(self.config).pushProduct(nextWorker,product)
        except Exception,e:
            print "got error",e," while pushProduct",e.__type__
            pass
        hyer.lock.unLock()


    def fetchProduct(self,nextWorker):
        '''
        取回某个worker线程要完成的工作
        '''
        #print "leader.fetchProduct() called"
        #hyer.log.info("try to fetch product")
        hyer.lock.lock("fetchProduct")
        try:
            tmp=hyer.production_db.ProductionDb(self.config).popProduct(nextWorker)
        except Exception,e:
            print "error while fetchProduct",e
            #hyer.log.track()
            tmp=None
        finally:
            pass
        hyer.lock.unLock()
        return tmp

class WorkerAutoLoadFromMysql(Worker):
    def fetchProduct(self,nextWorker):
        '''
        取回某个worker线程要完成的工作
        '''
        #print "leader.fetchProduct() called"
        #hyer.log.info("try to fetch product")
        try:
            self.conn=MySQLdb.connect(self.config["host"],self.config["user"],self.config["pass"],self.config["db"])
            self.cursor=self.conn.cursor(MySQLdb.cursors.DictCursor)
            self.cursor.execute("set names utf8")
            self.cursor.execute(self.config["sql"])
            rows=self.cursor.fetchall()
            j=0
            for row in rows:
                j+=1
                if self.config.has_key("new_product_id_from"):
                    row["__PRODUCT_ID__"]=str(row[self.config["new_product_id_from"]])
                else:
                    row["__PRODUCT_ID__"]=str(j)

                if isinstance(self.nextWorker,list):
                    for nw in self.nextWorker:
                        self.pushProduct(nw,row)
                else:
                    self.pushProduct(self.nextWorker,row)

        except Exception,e:
            print "error from workerAutoLoadFromMysql:"
            hyer.log.track()
            pass
        return None

    def run(self): 
        '''
        这种worker只干一遍活儿,就退出了.
        '''
        self.singleRun()

    def __del__(self):
        try:
            self.cursor.close()
        except:
            pass
        try:
            self.conn.close()
        except:
            pass

