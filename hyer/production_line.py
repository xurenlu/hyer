#coding:utf-8
import hyer.log
import hyer.worker
import sys,os
import threading
import time


class ProductionLine:
    workers=[]
    def __init__(self):
        pass
    def hireWorkers(self,workers):
        '''note:hireWorkers must be called after addLeader...'''
        for workerProperty in workers:
            worker=hyer.worker.Worker()
            worker.init(
                    workerProperty["name"],
                    self.Leader,
                    workerProperty["filters"],
                    workerProperty["products"],
                    workerProperty
                    )
            self.workers.append(worker)
            self.Leader.registerWorker(worker)
        pass
    def addLeader(self,Leader):
        '''note:hireWorkers must be called after addLeader...'''
        self.Leader=Leader
    def start(self):
        #self.Leader.run()
        threading.currentThread().setName("ProductionLine ")
        hyer.log.info("ProductionLine[%d] got %d workers" % (id(self),len(self.workers)))
        j=0
        for worker in self.workers:
            worker.setDaemon(True)
            worker.setName("worker-%d [%s]" % (j,worker.name))
            worker.start()
            hyer.log.info("%d:worker started:%s" % (j,str(id(worker))) )
            j=j+1
        while True:
            time.sleep(5)
            print "main thread..."
        for worker in self.workers:
            worker.join()

