#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Hyer project
    see  http://code.google.com/p/hyer/
"""

__author__ = "xurenlu"
__version__ = "0.57.1"
__copyright__ = "Copyright (c) 2008 renlu.xu "
__license__ = "new-style BSD"

import BeautifulSoup


def sig_exit():
	global spider
	sys.exit(0)
def handler(signum, frame):
	if signum == 2:
		sig_exit()
  else
    print "got new signal:%d" % signum
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

rrr= re.compile(".*[0-9\-]{5,}",re.I)
doc_id=0
def extract_doc(doc):
	global rrr,doc_id
	try :
		if (not rrr.match(doc["URI"]) ) :
			print "debug:",doc["URI"]," not matched\n"
			return None
		
		f=codecs.open("data/biz/yahoo/"+str(doc_id)+".txt","w+","UTF-8")
		f.write(doc["title"].decode("GBK","ignore").encode("UTF-8","ignore")+"\n")
		f.write("====subsplit====\n")
		html=doc["html"].decode("GBK","ignore").encode("utf-8","ignore")
		cnt=extMainText(html,0.03,None)
		cnt=cnt.decode("UTF-8","ignore")
		f.write(cnt)
		print "writed!\n"
		f.close()
		doc_id=doc_id+1
	except   Exception,(errno):
	   print "got an error:\n"
	   print errno
	   pass
signal.signal(2,handler)
spider=hyer.spider.spider({
"meta_server_host":"localhost",
"meta_server_port":8089,
"task":"biz",
"feed":"http://www.qiushibaike.com/",
"leave_domain":None,
"same_domain_regexp":r'http:\/\/www\.qiushibaike\.com\/',
"agent":"Hyer/0.5.7 (http://www.162cm.com/",
"db_path":"data/biz/",
"buckets":32,
"max_in_minute":120 #avoid to visite site too frequencently
})
#hyer.event.add_event("new_document",extract_doc)
spider.run_loop(); 
