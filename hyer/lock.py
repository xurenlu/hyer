#coding:utf-8

import threading
global globalMutex 
globalMutex=threading.Lock()

def lock():
    global globalMutex
    globalMutex.acquire()

def unLock():
    global globalMutex
    globalMutex.release()

