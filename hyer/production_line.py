#coding:utf-8
import hyer.log
import hyer.worker
import sys,os
import threading
import time
import gc

class ProductionLine:
    workers=[]
    def __init__(self,config):
        self.config=config
        pass
    def hireWorkers(self,workers):
        '''note:hireWorkers must be called after addLeader...'''
        for workerProperty in workers:
            if not workerProperty.has_key("products"):
                workerProperty["products"]=[]
            if not workerProperty.has_key("threads"):
                workerProperty["threads"]=1
            if not workerProperty.has_key("class"):
                workerProperty["class"]=hyer.worker.Worker

            for i in range(workerProperty["threads"]):
                worker=workerProperty["class"]()
                temp={}
                temp.update(self.config)
                temp.update(workerProperty)
                worker.init(
                        workerProperty["post"],
                        workerProperty["tools"],
                        workerProperty["products"],
                        workerProperty["nextWorker"],
                        temp
                        )
                self.workers.append(worker)
                for product in worker.products:
                    worker.pushProduct(worker.post,product)
                #self.Leader.registerWorker(worker)
        pass
    def addLeader(self,Leader):
        '''note:hireWorkers must be called after addLeader...'''
        self.Leader=Leader
    def start(self):
        #self.Leader.run()
        threading.currentThread().setName("ProductionLine ")
        hyer.log.info("ProductionLine[%d] got %d workers" % (id(self),len(self.workers)))
        j=0
        gc.enable()
        #gc.set_debug(gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE |  gc.DEBUG_INSTANCES | gc.DEBUG_OBJECTS)
        gc.set_debug(gc.DEBUG_UNCOLLECTABLE)
        for worker in self.workers:
            worker.setDaemon(True)
            worker.setName("worker-%s-%d" % (worker.post,j))
            worker.start()
            hyer.log.info("%d:worker started:%s" % (j,str(id(worker))) )
            j=j+1
        while True:
            time.sleep(3)
            f=open("/tmp/mem2.log","a+")

            f.write("gc.get_count():"+str(gc.get_count())+",len(gc.garbage):"+str(len(gc.garbage))+",\n")
            f.write(str(gc.garbage))
            f.close()

        for worker in self.workers:
            worker.join()

