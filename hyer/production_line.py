#coding:utf-8
import Queue
import hyer.log
import hyer.worker
import sys,os
import threading
import time


class ProductionLine:
    queue=Queue.Queue(10000)
    workers=[]
    def __init__(self):
        pass
    def hireWorkers(self,workers):
        '''note:hireWorkers must be called after addConsoleDesk...'''
        for workerProperty in workers:
            worker=hyer.worker.Worker()
            worker.init(
                    workerProperty["name"],
                    self.consoleDesk,
                    workerProperty["filters"],
                    workerProperty["products"],
                    workerProperty
                    )
            self.workers.append(worker)
            self.consoleDesk.registerWorker(worker)
        pass
    def addConsoleDesk(self,consoleDesk):
        '''note:hireWorkers must be called after addConsoleDesk...'''
        self.consoleDesk=consoleDesk
    def start(self):
        #self.consoleDesk.run()
        threading.currentThread().setName("ProductionLine ")

        hyer.log.info("started")
        hyer.log.info("ProductionLine[%d] got %d workers" % (id(self),len(self.workers)))
        for i in range(len(self.workers)):
            hyer.log.info("try to done worker %d" % i)
        j=0
        for worker in self.workers:
            worker.setDaemon(True)
            worker.setName("worker %d" % j )
            worker.start()
            hyer.log.info("%d:worker started:%s" % (j,str(id(worker))) )
            j=j+1
        while True:
            time.sleep(2)
            print "sleep gone"
        for worker in self.workers:
            worker.join()

