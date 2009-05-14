#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

__author__ = "Elias Soong (elias.soong@gmail.com)"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2008 Elias Soong"
__license__ = "New-style BSD"

import BeautifulSoup
def sig_exit():
  global spider
  #spider.print_urls()
  sys.exit(0)
def handler(signum, frame):
  if signum == 2:
    sig_exit()
    return None


#================================================
import sys, os
import hyer.document
import hyer.spider
import hyer.url_saver
import hyer.browser
import hyer.rules_monster
import hyer.event
import signal, os,time,re
import codecs
import sys
sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding("utf-8")
#print sys.getdefaultencoding()

#rrr= re.compile(".*[0-9\-]{5,}",re.I)
rrr=re.compile('http://bang.xianguo.com/feed\/[0-9]+/category.*',re.I)
rblog=re.compile('http://blog\..*',re.I)
rfeedsky=re.compile('http://feed\..*',re.I)
rxml=re.compile('.*xml',re.I)
rrss=re.compile('.*rss',re.I)

doc_id=0
def extract_doc(doc):
  global rrr,doc_id
  if rrr.match(doc["URI"]):
	  for c in doc["links"]:
	  	if rblog.match(c):
	  		print "new:",c
	  	if rfeedsky.match(c):
	  		print "new:",c
	  	if rxml.match(c):
	  		print "new:",c
	  	if rrss.match(c):
	  		print "new:",c

signal.signal(2,handler)
spider=hyer.spider.spider({
"task":"rss2",
"feed":"http://bang.xianguo.com/feed/463366/categoryId=163",
"leave_domain":False,
"same_domain_regexp":r'http:\/\/bang\.xianguo\.com\/',
"agent":"Hyer/0.5.4 (http://www.162cm.com/",
"db_path":"data/rss/",
"buckets":32,
"max_in_minute":120 #avoid to visite site too frequencently
})
hyer.event.add_event("new_document",extract_doc)
spider.run_loop(); 
