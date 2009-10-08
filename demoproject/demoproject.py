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

def run(configure):
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
