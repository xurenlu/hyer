#coding:utf-8

import threading
from hyer import pcolor
global globalMutex 
globalMutex=threading.Lock()
global locked
locked=False
def lock(reason=None):
    global globalMutex
    globalMutex.acquire()
    if reason==None:
        #print "locked by thread %s" % threading.currentThread().getName()
        pass
    else:
        #print "locked by thread %s because:%s" % (threading.currentThread().getName(),
        #pcolor.pcolorstr( reason,pcolor.PHIGHLIGHT,pcolor.PCYAN,pcolor.PBLACK)
        #)
        pass

def unLock():
    global globalMutex
    globalMutex.release()
    #print "unlocked by thread %s" % threading.currentThread().getName()

