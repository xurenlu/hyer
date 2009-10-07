#coding:utf-8
import threading
import time
import copy
import random
import hyer.singleton
import hyer.production_db

class Leader():

    workers=[]
    def __init__(self,config):
        self.config=config

    #def registerWorker(self,worker):
    #    '''登记一个工人/worker
    #    '''
    #    for product in worker.products:
    #        worker.pushProduct(worker.post,product)

    #    hyer.lock.lock("register worker")
    #    self.workers.append(worker)
    #    hyer.lock.unLock()

