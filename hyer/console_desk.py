#coding:utf-8

import threading
import hyer.singleton
class ConsoleDesk:
    def __init__(self,config={}):
        self.config=config
        self.productsToHandle={}
        pass
    def reportDone(self,task):
        pass
    def registerWorker(self,worker):
        '''登记一个工人/worker
        '''
        self.productsToHandle[worker.name]=worker.products
    def pushProduct(self,nextWorker,product):
        self.productsToHandle[nextWorker].append(product)
        pass
    def fetchProduct(self,nextWorker):
        '''
        取回某个worker线程要完成的工作
        '''
        try:
            return self.productsToHandle[nextWorker].pop(0)
        except:
            return None
        pass
