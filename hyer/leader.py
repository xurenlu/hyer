#coding:utf-8

import threading
import hyer.singleton
import hyer.lock
import time
class Leader(threading.Thread):
    productsToHandle={}
    workers=[]
    def reportDone(self,task):
        pass
    def registerWorker(self,worker):
        '''登记一个工人/worker
        '''
        hyer.lock.lock("register worker")
        self.productsToHandle[worker.name]=worker.products
        self.workers.append(worker)
        hyer.lock.unLock()
    def pushProduct(self,nextWorker,product):
        hyer.lock.lock("pushProduct")
        try:
            self.productsToHandle[nextWorker].append(product)
        except:
            pass
        hyer.lock.unLock()
        pass
    def __str__(self):
        return str(self.productsToHandle)
    def fetchProduct(self,nextWorker):
        '''
        取回某个worker线程要完成的工作
        '''
        #hyer.log.info("try to fetch product")
        hyer.lock.lock("fetchProduct")
        try:
            tmp=self.productsToHandle[nextWorker].pop(0)
        except Exception,e:
            #print self.productsToHandle[nextWorker]
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
