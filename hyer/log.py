#coding:utf-8
import hyer.singleton
import logging
from hyer import pcolor
import time
import threading
import hyer.lock
'''
colorful log text.
writer log messages to std.err  default 
specific a file to write it to a file
example code:
log.info("hi,baby")
log.error("hi,baby")
log.debug("hi,baby")
'''
def info(msg,file=None):
    _gen_msg("INFO",pcolor.PGREEN,msg,file)
def error(msg,file=None):
    _gen_msg("EROR",pcolor.PRED,msg,file)
def debug(msg,file=None):
    _gen_msg("DEBG",pcolor.PYELLOW,msg,file)

def _gen_msg(symbol,color,msg,file=None):
    hyer.lock.lock()
    thread=""
    tmp=""
    thread=",thread:%s,total threads:%d" % (
                str(threading.currentThread().getName()),
                threading.activeCount()
            )
    tmp="[%s] %s %s %s" % (symbol,time.ctime(),msg,thread)
    tmp="%s" % pcolor.pcolorstr(tmp,pcolor.PHIGHLIGHT,color,pcolor.PBLACK)
    print tmp
    hyer.lock.unLock()
    
