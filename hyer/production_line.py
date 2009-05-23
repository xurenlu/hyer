#coding:utf-8
import Queue
class ProductionLine:
    queue=Queue.Queue(10000)
    workers=[]
    def __init__(self):
        pass
    def addWorker(self,worker):
        self.workers.append(worker)
        pass
    def addWorkers(self,workers):

        pass
    def addConsoleDesk(self,consoleDesk):
        self.consoleDesk=consoleDesk
    def start(self):
        pass
    def run(self):
        #self.consoleDesk.run()
        for worker in self.workers:
            worker.setDaemon(True)
            worker.start()
         
