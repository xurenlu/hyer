#!/usr/bin/python
#coding:utf-8

STA_DONE=128
STA_ERR=1
#'''没有新任务时就休息2秒'''
REST_TIME=4

import time
import threading
import Queue
import hyer.log
import hyer.lock

class Worker(threading.Thread):
    '''
    Worker class 
    工人们从控制台取回下一步需要做的任务[原料],完成处理,再把原料交给控制台。
    工人们从控制台取任务时，有可能控制台返回说接下来没有任务需要完成。这时不能马上又去轮询，而是过n秒钟后再去询问,避免过度的空询问将consoleDesk堵塞.
    每一个工人都需要知道:当前要完成的任务号,

    '''
    def init(self,name,consoleDesk,filters,products,config={}):
        self.name=name
        self.consoleDesk=consoleDesk
        self.filters=filters
        self.products=products
        self.config=config
        self.nextWorker=config["nextWorker"]
        #for product in products:
        #    self.consoleDesk.pushProduct(self.name,product)
        #pass
    def requestNewTask(self):
        '''当前工人主动去请求任务'''
        pass
    def addTask(self,product):
        '''
        给当前工人指派任务
        '''
        self.products.append(product)
        pass

    def applyProducts(self,products):
        '''
        This method simply set the workers products to finish.
        as a rule,use this method to specific the first worker in the production line.
        这个方法直接设定当前worker所需要完成的产品
        一般情况下适用于某条流水线上最先开始干活的那个..
        ''' 
        self.products=products
    def addFilters(self,filters):
        self.filters.extend(filters)
    def addFilter(self,filter):
        self.filters.append(filter)
    def process(self,product):
        '''处理一件产品/加工一个作业'''
        for filter in self.filters:
            try:
                product=filter["class"](filter).run(product)
            except hyer.error.ExitLoopError,e:
                print "error caught:",e
                return False
        return product
    def report(self,status=STA_DONE):
        pass
    def finishOneProduct(self):
        '''
        完成了一件产品
        通知流水线的下一个工人可以继续干活了
        '''
        pass
    def run(self):
        while True:
            time.sleep(REST_TIME)
            hyer.log.info("worker got new loop operation")
            try:
                hyer.lock.lock()
                product=self.consoleDesk.fetchProduct(self.name)
                hyer.lock.unLock()
                if product == None:
                    hyer.log.debug("worker got null product" )
                else:
                    hyer.log.info("worker got new product")
                    output=self.process(product)
                    if isinstance(output,list):
                        for outproduct in output:
                            try:
                                hyer.lock.lock()
                                self.consoleDesk.pushProduct(self.nextWorker,outproduct)
                                hyer.lock.unLock()
                            except Exception,ep:
                                hyer.log.error("pushProduct error:%s" % ep)
                    else:
                        try:
                            hyer.lock.lock()
                            self.consoleDesk.pushProduct(self.nextWorker,output)
                            hyer.lock.unLock()
                        except Exception,ep:
                            hyer.log.error("pushProduct error:%s" % ep)

            except Exception,e:
                hyer.log.error("fetchProduct() failed:%s" % e )