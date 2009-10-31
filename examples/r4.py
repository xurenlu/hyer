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
import hyer.tool
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
"""
"""

__author__ = "xurenlu"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2008 xurenlu"
__license__ = "LGPL"

def sig_exit():
    print "[end time]:"+str(time.time())
    print hyer.pcolor.pcolorstr("CAUGHT SIG_EXIT signal,exiting...",hyer.pcolor.PHIGHLIGHT,hyer.pcolor.PRED,hyer.pcolor.PBLACK)
    sys.exit()

    sys.exit(0)
def handler(signum, frame):
    sig_exit()
    if signum == 3:
        sig_exit()
    if signum == 2:
        sig_exit()
    if signum == 9:
        sig_exit()
        return None
import signal, os,time,re
signal.signal(signal.SIGINT,handler)
signal.signal(signal.SIGTERM,handler)
signal.signal(3,handler)

#如果子进程退出时主进程不需要处理资源回收等问题
#这样可以避免僵尸进程
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding("utf-8")

#pid
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

start_time=time.time()
print "[start time]:"+str(start_time)

def at_exit():
    end_time=time.time()
    print "[end time]:"+str(end_time)
    print "[cost time]:"+str(end_time-start_time)
    print "\n=========================\n"

atexit.register(at_exit)

def usage():
    print 'usage:',sys.argv[0],' [-H mysql-host] [-d mysql-database] [-u mysql-user] [-p mysql-pass] -i start-url [-r url-regexp-to-visit] [-c cachedir] [-e encoding] [-t threshold]' 
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

if not configure.has_key("index"):
    usage()
    sys.exit()
if configure.has_key("regexp"):
    configure["regexp"]=re.compile(configure["regexp"])
else:
    import urlparse
    urls=urlparse.urlparse(configure["index"])
    configure["regexp"]=re.compile( str(urls.scheme)+"://"+str(urls.netloc))

configure["threshold"]= float(configure["threshold"])
print "\n\nstart with:\n"
print configure
print "\n\n"


workers=[
            {
                "post":"gen_list",
                "nextWorker":["visit_url"],
                "threads":1,
                "no_loop":True,
                "tools":[
                    {
                        "class":hyer.tool.UrlListGeneratorTool,
                        "template":"url_template",
                        "maxpage":"max",
                        "to":"urls"
                    },
                    {
                        "class":hyer.tool.TaskSplitTool,
                        "from":"urls",
                        "to":"url",
                        #"new_product_id_from":hyer.helper.peeker([])
                    },
                ]
            },
            {
                "post":"visit_url",
                "nextWorker":[],
                "threads":1,
                "tools":[
                {
                    "class":hyer.tool.UrlFetchTool,
                    "from":"url",
                    "to":"html",
                    "encoding":"GBK",
                    "db_path":"/tmp/"
                },
                {
                    "class":hyer.tool.IconvTool,
                    "f":"GBK",
                    "t":"UTF-8",
                    "from":"html",
                    "to":"html"
                },
                {
                    "class":hyer.tool.ReplaceTool,
                    "from":hyer.helper.peeker(["html"]),
                    "to":"html",
                    "replace_from":"\n",
                    "replace_to":""
                },
                {
                    "class":hyer.tool.RegexpExtractTool,
                    "regexp":re.compile(r'''<td style='font-size:14px;color:#ffffff' align=center>\s+<b>(.*)</b>\s+</td>.*<td valign=top class=wz12_8685>\s*?(.*?)</td>''', re.I|re.M),
                    "from":"html",
                    "to":"data",
                    "matches":[
                        {
                            "to":"title",
                            "index":hyer.helper.peeker([0,0])
                        },
                        {
                            "to":"body",
                            "index":hyer.helper.peeker([0,1])
                        }
                    ]
                },
                {
                    "class":hyer.tool.DeleteItemTool,
                    "delete_items":["html","url_template"]
                },
                {
                    "class":hyer.dbwriter.MySQLWriter,
                    "fields":["url","title","body"],
                    "host":configure["host"],
                    "user":configure["user"],
                    "pass":configure["pass"],
                    "db":configure["db"],
                    "table":"sohuall"
                }
                ]
            }
        ]





#<td style='font-size:14px;color:#ffffff' align=center></td>
#<td valign=top class=wz12_8685></td>
hyer.sl.workers_init(workers)
hyer.sl.init_tasks("gen_list", {
                    "url_template":"http://act1.baobao.sohu.com/expert/article.php?id=_page_",
                    "max":1545,
                    "__PRODUCT_ID__":"start"
                })
stackless.run()
