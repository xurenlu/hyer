#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#================================================
import sys
sys.path.append('/usr/lib/python2.5/site-packages/')
sys.path.append('/usr/lib/python2.6/dist-packages/')
sys.path.append("/var/lib/python-support/python2.5/")
sys.path.append("/var/lib/python-support/python2.6/")
import  stackless,sys, os,atexit
import hyer.document
import hyer.browser
import hyer.rules_monster
import hyer.event
import hyer.vsr
import hyer.source
import hyer.tool
import hyer.builders
import hyer.helper
import hyer.dbwriter
import hyer.production_line
#import hyer.worker
import hyer.leader
import hyer.singleton
import hyer.log
#import codecs
import sys,getopt
import json
import re
import threading
#import hyer.break_handler
import hyer.pcolor
import hyer.sl
import signal, os,time,re
import imp

"""
"""

__author__ = "xurenlu"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2008 xurenlu"
__license__ = "LGPL"

def sig_exit():
    """ handle the exit signal
    """
    print "[end time]:"+str(time.time())
    print hyer.pcolor.pcolorstr("CAUGHT SIG_EXIT signal,exiting...",hyer.pcolor.PHIGHLIGHT,hyer.pcolor.PRED,hyer.pcolor.PBLACK)
    sys.exit()

def handler(signum, frame):
    """
    handle signals
    """
    sig_exit()
    if signum == 3:
        sig_exit()
    if signum == 2:
        sig_exit()
    if signum == 9:
        sig_exit()
        return None

def prepare_taskfile(taskfile):
    """Attempt to load the taskfile as a module.
    """
    path = os.path.dirname(taskfile)
    taskmodulename = os.path.splitext(os.path.basename(taskfile))[0]
    fp, pathname, description = imp.find_module(taskmodulename, [path])
    print "fp:",fp,",pathname:",pathname,",desc:",description
    try:
        return imp.load_module(taskmodulename, fp, pathname, description)
    finally:
        if fp:
            fp.close()

def handle_pid():
    """
    handle pid files
    """
    pid=os.getpid()
    pidfile= "/tmp/run.generic.pid"
    try:
        lastpid=int(open(pidfile).read())
    except:
        lastpid=0
        pass
    try:
        if lastpid>0:
            os.kill(lastpid,9)
    except:
        pass
    fp=open(pidfile,"w")
    fp.write(str(pid))
    fp.close()

def at_exit():
    """
    hook of exit
    """
    end_time=time.time()
    print "[end time]:"+str(end_time)
    print "[cost time]:"+str(end_time-start_time)
    print "\n=========================\n"

def usage():
    print 'usage:',sys.argv[0],' [-H mysql-host] [-d mysql-database] [-u mysql-user] [-p mysql-pass] [-i start-url] [-r url-regexp-to-visit] [-c cachedir] [-e encoding] [-t threshold] taskfile' 



signal.signal(signal.SIGINT,handler)
signal.signal(signal.SIGTERM,handler)
signal.signal(3,handler)

#如果子进程退出时主进程不需要处理资源回收等问题
#这样可以避免僵尸进程
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding("utf-8")



start_time=time.time()
print "[start time]:"+str(start_time)
atexit.register(at_exit)
try:
    opts, args= getopt.getopt(sys.argv[1:],"hH:d:u:p:i:r:c:e:t:",
            ["help",
            "host=",
            "db=",
            "user=",
            "pass=",
            "index=",
            "regexp=",
            "cachedir=",
            "encoding=",
            "threshold="
            ])
except getopt.GetoptError,e:
    # print help information and exit:
    print "arguments parse error:",e
    usage()
    sys.exit()
configure={
    "host":"localhost",
    "db":"hyer",
    "user":"root",
    "pass":"",
    "cachedir":"./cachedir/",
    "encoding":"GBK",
    "threshold":0.015
    }
for o,a in opts:
    print "o:",o,",a:",a
    if o in ('-h','--help'):
        usage()
        sys.exit()
    if o in ("-u","--user"):
        configure["user"]=a
    if o in ("-p","--pass"):
        configure["pass"]=a
    if o in ("-H","--host"):
        configure["host"]=a
    if o in ("-d","--db"):
        configure["db"]=a
    if o in ("-i","--index"):
        configure["index"]=a
    if o in ("-r","--regexp"):
        configure["regexp"]=a
    if o in ("-c","--cachedir"):
        configure["cachedir"]=a
    if o in ("-e","--encoding"):
        configure["encoding"]=a
    if o in ("-t","--threshold"):
        configure["threshold"]=a

#if not configure.has_key("index"):
#    usage()
#    sys.exit()
#if configure.has_key("regexp"):
#    configure["regexp"]=re.compile(configure["regexp"])
#else:
#    import urlparse
#    urls=urlparse.urlparse(configure["index"])
#    configure["regexp"]=re.compile( str(urls.scheme)+"://"+str(urls.netloc))
#configure["threshold"]= float(configure["threshold"])

if len(sys.argv)==1:
    usage()
    sys.exit()

taskfile=sys.argv[-1]
k=prepare_taskfile(taskfile)
print k.run(configure)
print "k:",k
print "\n\nstart with:\n"
print configure
print "\n\n"


