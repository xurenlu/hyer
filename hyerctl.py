#!/usr/local/bin/python.stackless
# -*- coding: utf-8 -*-
#================================================
import sys
sys.path.append('/usr/lib/python2.5/site-packages/')
sys.path.append('/usr/lib/python2.6/dist-packages/')
sys.path.append("/var/lib/python-support/python2.5/")
sys.path.append("/var/lib/python-support/python2.6/")
import stackless,sys, os,atexit
import sys,getopt
import json
import threading
import signal, os,time,re
import imp
import shutil

import hyer.document
import hyer.browser
import hyer.rules_monster
import hyer.event
import hyer.tool
import hyer.helper
import hyer.dbwriter
import hyer.singleton
import hyer.log
import hyer.pcolor
import hyer.sl

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

def inittask(task):
    """init a task and create empty files for you 
    """
    try:
        os.mkdir(task,0755)
    except:
        pass
    try:
        shutil.copyfile("share/templates/project.py","%s/%s.py" % (task,task) )
    except:
        pass
    try:
        shutil.copyfile("share/templates/config.py","%s/config.py" % task )
    except:
        pass

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
    print "usage:\t",sys.argv[0],' init task' 
    print "usage:\t",sys.argv[0],' run taskfile' 
    print "usage:\t",sys.argv[0],' help' 



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

if len(sys.argv)<2:
    usage()
    sys.exit()

cmd=sys.argv[1].lower()
if cmd == "help" :
    usage()
    sys.exit()

elif cmd == "runfile":
    '''run a single file'''
    print "[start time]:"+str(start_time)
    atexit.register(at_exit)
    taskfile=sys.argv[-1]
    k=prepare_taskfile(taskfile)
    k.run({})
    stackless.run()

elif cmd == "run":
    '''run a project '''
    print "[start time]:"+str(start_time)
    atexit.register(at_exit)
    taskfile=sys.argv[-1]

elif cmd == "init":
    task=sys.argv[-1]
    inittask(task)
else:
    usage()
    sys.exit()
