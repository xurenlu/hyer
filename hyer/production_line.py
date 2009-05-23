#coding:utf-8
import Queue
import hyer.log
import hyer.worker
import sys,os
import threading
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
                    workerProperty["products"]
                    )
            self.workers.append(worker)
        pass
    def addConsoleDesk(self,consoleDesk):
        '''note:hireWorkers must be called after addConsoleDesk...'''
        self.consoleDesk=consoleDesk
    def start(self):
        #self.consoleDesk.run()
        log=hyer.log.Log()
        log.info("started")
        log.info("ProductionLine[%d] got %d workers" % (id(self),len(self.workers)))
        for worker in self.workers:
            worker.setDaemon(True)
            worker.start()
            hyer.log.Log().info("worker[%d] started,thread[%s],threadid[%d]" % ( id(worker),str(threading.currentThread()),id(threading.currentThread()) ) )
        for worker in self.workers:
            worker.join()

