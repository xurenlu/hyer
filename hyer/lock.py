#coding:utf-8

import threading
from hyer import pcolor
global globalMutex 
globalMutex=threading.Lock()
global locked
locked=False
def lock(reason=None):
    global globalMutex
    if reason==None:
        print "locked by thread %s" % threading.currentThread().getName()
    else:
        print "locked by thread %s because:%s" % (threading.currentThread().getName(),
        pcolor.pcolorstr( reason,pcolor.PHIGHLIGHT,pcolor.PCYAN,pcolor.PBLACK)
                )

    globalMutex.acquire()

def unLock():
    global globalMutex
    print "unlocked by thread %s" % threading.currentThread().getName()
    globalMutex.release()

