#!/usr/bin/python
#coding:utf-8

STA_DONE=128
STA_ERR=1
#'''没有新任务时就休息2秒'''
REST_TIME=2

import time
import threading
import Queue
class Worker(threading.Thread):
    '''
    Worker class 
    工人们从控制台取回下一步需要做的任务[原料],完成处理,再把原料交给控制台。
    工人们从控制台取任务时，有可能控制台返回说接下来没有任务需要完成。这时不能马上又去轮询，而是过n秒钟后再去询问,避免过度的空询问将consoleDesk堵塞.
    每一个工人都需要知道:当前要完成的任务号,

    '''
    def init(self,consoleDesk,filter,config={}):
        self.consoleDesk=consoleDesk
        self.filter=filter
        self.config=config
        self.products=Queue.Queue()
        pass
    def requestNewTask(self):
        '''当前工人主动去请求任务'''
        pass
    def addTask(self,product):
        '''
        给当前工人指派任务
        '''
        self.products.append(product)
        pass
    def addFilters(self,filters):
        self.filters.extend(filters)
    def addFilter(self,filter):
        self.filters.append(filter)
    def process(self):
        pass
    def report(self,status=STA_DONE):
        pass
    def finishOneProduct(self):
        '''
        完成了一件产品
        通知流水线的下一个工人可以继续干活了
        '''
        pass
    def pop(self):
        '''
        从待完成任务中取中一件来
        '''

    def run(self):
        while True:
            try:
                product=self.pop()
                if product == None:
                    time.sleep(REST_TIME)
                else:
                    self.process(product)
            except:
                time.sleep(REST_TIME)
        pass
