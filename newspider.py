# -*- coding: utf-8 -*-
#================================================
import sys
sys.path.append('/usr/lib/python2.5/site-packages/')
sys.path.append('/usr/lib/python2.6/dist-packages/')
sys.path.append("/var/lib/python-support/python2.5/")
sys.path.append("/var/lib/python-support/python2.6/")
sys.path.append("/usr/share/pyshared/")
sys.path.append("/usr/lib/pymodules/python2.6/")
import sys, os,atexit
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
import hyer.urldb
import hyer.spider
#import hyer.sl

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

def inittask(task,type="web"):
    """init a task and create empty files for you 
    """
    try:
        os.mkdir(task,0755)
    except Exception,e:
        print "exception:",e
        pass
    try:
        shutil.copyfile("share/templates/project-%s.py" % type,"%s/%s.py" % (task,task) )
    except Exception,e:
        print "exception:",e
        pass
    try:
        shutil.copyfile("share/templates/config-%s.py" % type,"%s/config.py" % task )
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


import pdb
#pdb.set_trace()
conf={
    "db_path":"./tmp/",
    "feed":"http://bangpai.taobao.com/group/discussion/22023--1.htm",
    "max_in_minute":60,
    "agent":"Mozilla/Firefox",
    "same_domain_regexps":[re.compile("http://bangpai.taobao.com/group/discussion/22023--\d+.htm"),
                           re.compile("http://bangpai.taobao.com/group/thread/22023-\d+.htm") 
                          ],
    "url_db":hyer.urldb.Urldb_mysql({"host":"localhost","user":"renlu","pass":"","db":"hyer"}),
    "task":"cyxfbangpai",
    "leave_domain":False
}
def cb_new_document(doc):
    if re.match(r'http:\/\/bangpai.taobao.com\/group\/thread\/22023-\d+.htm',doc["URI"]):
        print "matched uri:",doc["URI"]
        #运行iconvtool 来转为中文
        iconvtool = hyer.tool.IconvTool( {
            "f":"GBK",
            "t":"UTF-8",
            "from":"html",
            "to":"html"
        })
        newdoc = iconvtool.run(doc)
        btstool = hyer.tool.BeautifulSoupMultiNodeTool({
            "class":hyer.tool.BeautifulSoupMultiNodeTool,
            "from":"html",
            "to":"content_nodes",
            "tagname":"div",
            "attrs":{"class":re.compile("ke-post")}
        })

        newdoc = btstool.run(newdoc)
        try:
            content = newdoc["content_nodes"][0]
            writer = hyer.dbwriter.MySQLWriter( {
                "class":hyer.dbwriter.MySQLWriter,
                "fields":["url","content"],
                "host":"localhost",
                "user":"renlu",
                "pass":"",
                "db":"hyer",
                "table":"posts",
                "insert_method":"REPLACE" # or replace
            })
            newhash={"content":content,"url":newdoc["URI"]}
            writer.run(newhash)
        except Exception,e:
            print "got new exception:",e
            sys.exit()
            pass
    else:
        print "not matched uri:",doc["URI"]

hyer.event.add_event("new_document",cb_new_document)
spider=hyer.spider.spider(conf)
spider.start(0)
