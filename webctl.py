#!/usr/bin/python
# -*- coding: utf-8 -*-
#================================================
#copyright:GPL 
from __future__ import with_statement 
"""
"""

__author__ = "xurenlu"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2008 xurenlu"
__license__ = "LGPL"

import subprocess 
import sys
sys.path.append('/usr/lib/python2.5/site-packages/')
sys.path.append('/usr/lib/python2.6/dist-packages/')
sys.path.append("/var/lib/python-support/python2.5/")
sys.path.append("/var/lib/python-support/python2.6/")
sys.path.append("/usr/share/pyshared/")
sys.path.append("/usr/lib/pyshared/python2.5/")
sys.path.append("/usr/lib/pyshared/python2.6/")
import sys, atexit
import signal,time,re
import imp
import getopt 

import hyer.document
import hyer.event
import hyer.dbwriter
import hyer.pcolor
import hyer.spider
import hyer.misc
import hyer.config

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

def at_exit():
    """
    hook of exit
    """
    end_time=time.time()
    print "[end time]:"+str(end_time)
    print "[cost time]:"+str(end_time-start_time)
    print "\n=========================\n"

def usage():
    print "\n"
    print "Hyer crawler     version ",hyer.__version__
    print "Author:",hyer.__author__
    print "Homepage:",hyer.__homepage__
    print "\n\n\n"
    
    sys.exit(0)




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


optlist,args=getopt.getopt(sys.argv[1:],"c:h")

config={"conf":None,"help":False}
for (c,v) in optlist:
    if c == "-c":
        config["conf"]=v
    if c == "-h":
        config["help"]=True

if config["help"]:
    usage()




conf={
        "db_path":"./tmp/",
        "feed":"http://www.xinhuanet.com/newscenter/index.htm",
        #"feed":"http://localhost/htests/",
        "max_in_minute":60,
        "agent":"Mozilla/Firefox",
        "same_domain_regexps":[re.compile("http://www.xinhuanet.com/")],
        #"same_domain_regexps":[re.compile("http://localhost/htests/")],
        "url_db":hyer.urldb.Urldb_mysql({"host":"localhost","user":"root","pass":"","db":"hyer2"}),
        "task":"profiletest",
        "leave_domain":False,
        "document":hyer.document.SimpleHTMLDocument
        }
spider=hyer.spider.spider(conf)

writerconf={
        "host":"localhost",
        "user":"root",
        "pass":"",
        "db":"hyer2",
        "table":"xinhuall",
        "fields":["url","content","tags","charset"]
    }
wdb=hyer.dbwriter.MySQLWriter(writerconf)

def handle_new_doc(doc):
    print "handle new doc:"
    if doc["charset"]!="UTF-8":print "[notice] charset not utf8 but ",doc["charset"],":",doc["URI"]
    doc["url"]=doc["URI"]
    #doc["tags"]=hyer.misc.gettags(doc["content"])
    #doc["update_time"]=9200
    #wdb.run(doc)

def filter_new_doc(doc):
    r=re.compile(".*content_[0-9]+\.html$")
    if r.match(doc["URI"]):
        doc["update_time"]=31635000
    else:
        doc["update_time"]=7200

    return doc

def start():
    spider=hyer.spider.spider(conf)
    hyer.event.add_event("new_document",handle_new_doc)
    hyer.event.add_filter("new_document",filter_new_doc)
    spider.run_loop()


start()
