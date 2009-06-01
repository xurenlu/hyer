#!/usr/bin/python
# -*- coding: utf-8 -*-
#================================================
import sys, os
import hyer.document
import hyer.browser
import hyer.rules_monster
import hyer.event
import hyer.vsr
import hyer.source
import hyer.filter
import hyer.builders
import hyer.helper
import hyer.dbwriter
import hyer.production_line
import hyer.worker
import hyer.leader
import hyer.singleton
import hyer.log
import codecs
import sys
import json
import re
import threading
#import hyer.break_handler
import hyer.pcolor
"""
"""

__author__ = "xurenlu"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2008 xurenlu"
__license__ = "LGPL BSD"

def sig_exit():
    print hyer.pcolor.pcolorstr("CAUGHT SIG_EXIT signal,exiting...",hyer.pcolor.PHIGHLIGHT,hyer.pcolor.PRED,hyer.pcolor.PBLACK)
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

global g_mutex
g_mutex=None
g_mutex = threading.Lock()
print g_mutex
Leader=hyer.leader.Leader()
workers=[
        {
            "post":"UrlFetch",
            "nextWorker":["TextGrabber","LinksGrabber"],
            "threads":1,
            "products":[
                {
                    "url":"http://business.sohu.com/"
                }
                ],
            "filters":[
                {
                    "class":hyer.filter.DisplayFilter,
                },
                {
                    "class":hyer.filter.UniqueCheckFilter,
                    "from":"url",
                },
                {
                    "class":hyer.filter.UrlFetchFilter,
                    "to":"html",
                    "agent":"Mozilla/Firefox 3.1",
                    "from":"url",
                    "db_path":"./db_sohu/"
                },
                {
                    "class":hyer.filter.IconvFilter,
                    "f":"GBK",
                    "t":"UTF-8",
                    "from":"html",
                    "to":"html"
                },
                {
                    "class":hyer.filter.TidyHTMLFilter,
                    "from":"html",
                    "to":"html",
                    "input_encoding":"utf8",
                    "output_encoding":"utf8"
                }
                ]
            },
            {
                "post":"LinksGrabber",
                "threads":1,
                "nextWorker":["GenNewUrls"],
                "products":[],
                "filters":[
                {
                    "class":hyer.filter.ScanLinksFilter,
                    "from":"html",
                    "uri_field":"url",
                    "to":"urls",
                    "validate_url_regexps":[ re.compile('http:\/\/business\.sohu\.com\/'), re.compile('http:\/\/money\.sohu\.com')]
                },
                {
                    "class":hyer.filter.TaskSplitFilter,
                    "from":"urls",
                    "to":"urls"
                }
                ]
            },
            {
                "post":"GenNewUrls",
                "nextWorker":["UrlFetch"],
                "products":[],
                "filters":[
                {
                    "class":hyer.filter.DeleteItemFilter,
                    "delete_items":["html"]
                },
                {
                    "class":hyer.filter.ReMixArrayFilter,
                    "from":"urls",
                    "to":"url",
                    "column":"url"
                },
                {
                    "class":hyer.filter.ReMixArrayFilter,
                    "from":"urls",
                    "to":"text",
                    "column":"text"
                },
                {
                    "class":hyer.filter.DeleteItemFilter,
                    "delete_items":["urls"]
                }
                ]
            },
            {
                "post":"TextGrabber",
                "threads":1,
                "nextWorker":None,
                "products":[],
                "filters":[
                {
                    "class":hyer.filter.ExtMainTextFilter,
                    "from":"html",
                    "to":"maintext",
                    "threshold":0.03
                },
                {
                    "class":hyer.dbwriter.MySQLWriter,
                    "fields":["maintext","url","text"],
                    "host":"localhost",
                    "user":"root",
                    "pass":"",
                    "db":"hyer",
                    "table":"sohudata"
                }
                ]
            }
        ]
productionLine=hyer.production_line.ProductionLine()
productionLine.addLeader(Leader)
productionLine.hireWorkers(workers)
productionLine.start()
print "total:%d" % threading.activeCount()
