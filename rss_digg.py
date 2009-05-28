#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
"""

"""

__author__ = "Elias Soong (elias.soong@gmail.com)"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2008 Elias Soong"
__license__ = "New-style BSD"

import BeautifulSoup
def sig_exit():
    sys.exit(0)
def handler(signum, frame):
    if signum == 2:
        sig_exit()
    return None


#================================================
import sys, os
import hyer.document
import hyer.spider
#import hyer.url_saver
import hyer.browser
import hyer.rules_monster
import hyer.event
import signal, os,time,re
import codecs
import sys
import extmain.extmain
sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding("utf-8")
#print sys.getdefaultencoding()

import subprocess
import os

def tidy(jhtml):
    j=os.tmpnam()
    ft=open(j,"w+")
    ft.write(jhtml)
    ft.close()
    with os.tmpfile() as temp:
        with open(os.devnull,"w" ) as null:
            print >>temp,jhtml
            temp.seek(0)
            rhtml=subprocess.Popen(
            #["tidy", "-utf8","-asxhtml"],
            ["./tidy.php", j],
            stdin=temp,
            stderr=null,
            stdout=subprocess.PIPE
            ).communicate()[0]
    begin="<body>"
    os.unlink(j)
    return rhtml
    return html[html.find(begin)+len(begin):html.rfind("</body>")].strip()


uri_re=re.compile('.*n[\d]+\.shtml',re.I)

doc_id=0
def extract_doc(doc):
    global uri_re,doc_id
    if uri_re.match(doc["URI"]):
        print "got new url matchs.%s" % doc["URI"]
        html=doc["html"]
        html=html.decode("GBK","ignore").encode("UTF-8","ignore")
        xhtml=tidy(html)
        print "len:%d" % len(html) 
        print xhtml.__class__
        print len(xhtml)
        if xhtml==None:
            print "error:got none:"
            print "len:%d" % len(xhtml)
            sys.exit(0)
        try:
            main=extmain.extmain.extMainText(xhtml,0.03)
        except Exception,e:
            print "error occured while extMainText:%s" % e
            print xhtml
            return False
        f=open("/var/data/sohu/txt/%d.html" % doc_id,"w+")
        f.write(main)
        f.close()
    doc_id=doc_id+1 

signal.signal(2,handler)
spider=hyer.spider.spider({
"task":"sohucj",
"feed":"http://business.sohu.com/",
"leave_domain":False,
"same_domain_regexps":[ re.compile('http:\/\/business\.sohu\.com\/'), re.compile('http:\/\/money\.sohu\.com\/'), re.compile('http:\/\/stock\.sohu\.com\/') ],
"agent":"Hyer/0.5.4 (http://www.162cm.com/",
"db_path":"/var/data/sohu/",
"buckets":32,
"max_in_minute":10, #avoid to visite site too frequencently
"document":hyer.document.SimpleHTMLDocument,
})
hyer.event.add_event("new_document",extract_doc)
spider.run_loop(); 
#spider.start(10)
