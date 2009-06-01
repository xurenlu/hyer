#coding:utf-8
import threading
import time
import copy
import random
import hyer.singleton
import hyer.lock
import hyer.production_db
class Leader():
#threading.Thread):
    productsToHandle={}
    workers=[]
    def __init__(self,config):
        self.config=config
    def reportDone(self,task):
        pass
    def registerWorker(self,worker):
        '''登记一个工人/worker
        '''
        for product in worker.products:
            self.pushProduct(worker.post,product)
        #self.productsToHandle[worker.post]=worker.products

        hyer.lock.lock("register worker")
        self.workers.append(worker)
        hyer.lock.unLock()
    def pushProduct(self,nextWorker,product):
        '''
        将一份产品录入到库中.
        '''
        print "leader.pushProduct() called"
        tempProduct=copy.copy(product)
        hyer.lock.lock("pushProduct")
        try:
            hyer.production_db.ProductionDb(self.config).pushProduct(nextWorker,product)
            #self.productsToHandle[nextWorker].append(tempProduct)
        except Exception,e:
            print "error occured while pushProduct ",e
            pass
        hyer.lock.unLock()
        pass
    def __str__(self):
        return str(self.productsToHandle)
    def fetchProduct(self,nextWorker):
        '''
        取回某个worker线程要完成的工作
        '''
        print "leader.fetchProduct() called"
        #hyer.log.info("try to fetch product")
        hyer.lock.lock("fetchProduct")
        try:
            #if(len(self.productsToHandle[nextWorker])==0):
            #    hyer.lock.unLock()
            #    return None
            tmp=hyer.production_db.ProductionDb(self.config).popProduct(nextWorker)
            #index=random.randint(0,len(self.productsToHandle[nextWorker])-1)
            #tmp=self.productsToHandle[nextWorker].pop(index)
            hyer.lock.unLock()
            hyer.log.info("get products success")
            hyer.lock.lock("nothing")
        except Exception,e:
            print "error in leader:,",e
            hyer.lock.unLock()

            hyer.log.error("error: %s" % str(e))
            hyer.lock.lock("nothing")
            tmp=None
        finally:
            pass
        hyer.lock.unLock()
        return tmp
    def run(self):
        while True:
            for wk in self.workers:
                pass        
            time.sleep(2)
        pass
