#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

__author__ = "Elias Soong (elias.soong@gmail.com)"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2008 Elias Soong"
__license__ = "New-style BSD"

def sig_exit():
  global spider
  #spider.print_urls()
  sys.exit(0)
def handler(signum, frame):
  if signum == 2:
    sig_exit()
    return None
import signal, os,time,re
signal.signal(2,handler)


#================================================
import sys, os
import hyer.document
import hyer.spider
import hyer.browser
import hyer.rules_monster
import hyer.event
import hyer.vsr
import hyer.source
import hyer.filter
import hyer.builders
import hyer.helper
import hyer.dbwriter
import codecs
import sys
import json
sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding("utf-8")

builder_gen_categories= {
    "db_path":"/var/data/amazon/",
    "max_in_minute":10, #avoid to visite site too frequencently
    "document":hyer.document.Document,
    "rest_time":4,
    "data":{},
    "class":hyer.builders.Builder,
    "filters":[
    {
        "class":hyer.source.Generic,
#        "feed":"http://www.amazon.cn/mn/channel/480-9277404-6871849?ref=GT&pageletid=xinjiang&uid=480-9277404-6871849&channelCode=book",
        "feed":"http://www.162cm.com/",
        "agent":"Hyer/0.5.4 (http://www.162cm.com/"
    },
    {
        "class":hyer.filter.ExtractFilter,
        "from":"html",
        "to":"body",
        "starttag":"<body>",
        "endtag":"</body>",
        "ignorecase":True,
        "oeperate":"copy" #other value:move
    },
    {
        "class":hyer.filter.XpathFilter,
        "from":"body",
        "to":"catesstring",
        "xpath":"#lefttable ",
        "operate":"copy"
    },
    {
        "class":hyer.filter.MultiExtractFilter,
        "starttag":'<li class="cat-item',
        "endtag":"</li>",
        "from":"body",
        "to":"cates"
    },
    {
            "class":hyer.filter.DeleteItemFilter,
            "delete_items":["html","body"],
            "from":""
    },
    {
            "class":hyer.filter.InfoExtractFilter,
            "filters":[
                    {
                            "starttag":""
                    }
            ]
    },
    {
        "class":hyer.filter.DisplayFilter
    },
    {
        "class":hyer.filter.ExtractMultiFieldsFilter,
        "from":"cates",
        "to":"cates_info",
        "tags":[
            {
                "starttag":'<a href="',
                "endtag":'" title=',
                "to":"cate_url"
            },
            {
                "starttag":'>',
                "endtag":'<',
                "to":"cate_name"
            }
        ]
    }, 
    {
        "class":hyer.filter.DeleteItemFilter,
        "delete_items":["cates"],
        "from":""
    },
    {
        "class":hyer.filter.DeleteItemFilter,
        "from":"cates_info",
        "delete_items":[]
    },
    {
        "class":hyer.dbwriter.TextFileWriter,
        "from":"",
        "write_to":"/var/data/amazon/cates.json"
    },
    {
        "class":hyer.filter.ReMixArrayFilter,
        "from":"cates_info",
        "column":"cate_url",
        "to":"cate_urls"
    },
    {
        "class":hyer.dbwriter.LineAppendWriter,
        "from":"cate_urls",
        "write_to":"/var/data/amazon/cateurls.json"
    },
    {
        "class":hyer.filter.DisplayFilter
    }
    ]
}
builder_get_category_list={
    "data":{},
    "class":hyer.builders.FileRowsTaskBuilder,
    "taskfile":"/var/data/amazon/cateurls.json",
    "db_path":"/var/data/amazon/",
    "source":
        {
            "class":hyer.source.Source,
            #"agent":"Mozilla 4.0(windows NT 5.0) alextoolbar installed",
            "agent":"Mozilla/5.0 (X11; N; Linux 2.2.16-22smp i686; en-US; m18) Gecko/20001220",
            "startat":1,
            "step":1,
            "db_path":"/var/data/amazon/",
            "template":"template",
            "musthave":"&laquo; Previous Entries",
            "to":"maxpage",
            "from":"__ROW__"
        },
        "filters":[
        {
            "class":hyer.filter.AddStringFilter,
            "string":"/page/_page_",
            "side":"right",
            "from":"__ROW__",
            "to":"template"
        },
        {
            "class":hyer.filter.MaxPageGetterByStringFilter,
            "agent":"Mozilla/5.0 (X11; N; Linux 2.2.16-22smp i686; en-US; m18) Gecko/20001220",
            "startat":1,
            "step":1,
            "db_path":"/var/data/amazon/",
            "template":"template",
            "musthave":"&laquo; Previous Entries",
            "to":"maxpage",
            "from":"template"
        },
        {
            "class":hyer.filter.UrlListGeneratorFilter,
            "startat":1,
            "maxpage":"maxpage",
            "step":1,
            "template":"template",
            "to":"urllist",
        },
        {
            "class":hyer.filter.DisplayFilter
        },
        {
            "class":hyer.dbwriter.LineAppendWriter,
            "from":"urllist",
            "write_to":"/var/data/amazon/urls_1.json",
            "appendix":"__ID__",
        },
        {
            "class":hyer.filter.ExitLoopFilter
        },
        {
            "class":hyer.filter.ExitFilter
        },
        {
            "class":hyer.filter.UrlFetchFilter,
            "agent":"Mozilla/5.0 (X11; N; Linux 2.2.16-22smp i686; en-US; m18) Gecko/20001220",
            "db_path":"/var/data/amazon/",
            "to":"html",
            "from":"__ROW__"
        },
        {
            "class":hyer.filter.DeleteItemFilter,
            "delete_items":[],
            "from":""
        },
        {
            "class":hyer.filter.JsonDisplayFilter
        },
        {
            "class":hyer.dbwriter.JsonLineAppendWriter,
            "from":"",
            "write_to":"/var/data/amazon/allcates.json"
        },

        ]
    }

vs=hyer.vsr.VSR({
    "builders":[
        #builder_gen_categories,
        builder_get_category_list]
    });
vs.run()
#spider.start(10)
