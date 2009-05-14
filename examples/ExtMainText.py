#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ExtMainText: Parses HTML and filters non main text parts.

http://www.elias.cn/En/ExtMainText

ExtMainText parses a HTML document, keeps only html about main text, and 
filter advertisements and common menus in document.

Such module could help search engine focus on most valuable part of html
documents, and help page monitors and extractors just pay attension on most 
meaningful part.

The current implementation bases on the measure of html tag density, and 
determine the threshold according to historical experience. The original 
algorithm comes from http://www.xd-tech.com.cn/blog/article.asp?id=59

The "if __name__ == '__main__'" part of such module can be a usage sample of 
extmaintext.

Here, have some legalese:

Copyright (c) 2008, Elias Soong

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
	notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above
	copyright notice, this list of conditions and the following
	disclaimer in the documentation and/or other materials provided
	with the distribution.

  * Neither the name of the the Beautiful Soup Consortium and All
	Night Kosher Bakery nor the names of its contributors may be
	used to endorse or promote products derived from this software
	without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE, DAMMIT.

"""

__author__ = "Elias Soong (elias.soong@gmail.com)"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2008 Elias Soong"
__license__ = "New-style BSD"

import BeautifulSoup

def extMainText(html, threshold = 0.03, debug = False):
	"""
	Parses HTML and filters non main text parts.
	Return: html part of main text
	"""
	soup = BeautifulSoup.BeautifulSoup(html)
	soup = soup.body
	countDic = calcDensity(soup)
	if debug:
		print countDic
		print "======"
	maxSoup, textLen = getMainText(countDic, threshold)
	return unicode(maxSoup)

def getMainText(countDic, threshold):
	"""
	Get the longest html part with tag density smaller than threshold according 
	to density dictionary.
	Return: (soup object, max text length with small enough tag density)
	"""
	dens, tagNo, textLen, soup = countDic['self']
	if dens <= threshold:
		maxSoup = soup
		maxTextLen = textLen
	else:
		maxSoup = BeautifulSoup.BeautifulSoup("")
		maxTextLen = 0
	if countDic.has_key('child'):
		for childDic in countDic['child']:
			soup, textLen = getMainText(childDic, threshold)
			if textLen > maxTextLen:
				maxSoup = soup
				maxTextLen = textLen
	return (maxSoup, maxTextLen)

def calcDensity(soup):
	"""
	Count the number of html tags and the length of pure text information in a
	soup entity.
	Return: {'self': (tag density, number of tags, length of pure text, soup object), 
	'child': list of count dics for child entities }
	"""
	uni = unicode(soup)
	if isinstance(soup, BeautifulSoup.NavigableString):
		if uni.startswith("<!--"):
			return {'self': (0.0, 0, 0, soup)}
		return {'self': (0.0, 0, len(uni), soup)}
	if soup.name in ("script", "style"):
		return {'self': (1.0, 0, 0, BeautifulSoup.BeautifulSoup(""))}
	countTagNo = 1   # This is the current tag.
	countTextLen = 0
	dicList = []
	for content in soup.contents:
		dic = calcDensity(content)
		dicList.append(dic)
		tagNo, textLen = dic['self'][1:3]
		countTagNo += tagNo
		countTextLen += textLen
	density = countTextLen != 0 and float(countTagNo) / countTextLen or 1.0
	return {'self': (density, countTagNo, countTextLen, soup), 'child': dicList}

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
"task":"rss",
"feed":"http://www.qiushibaike.com/",
"leave_domain":True,
"same_domain_regexp":r'http:\/\/www\.qiushibaike\.com\/',
"agent":"Hyer/0.5.4 (http://www.162cm.com/",
"db_path":"data/biz/",
"buckets":32,
"max_in_minute":120 #avoid to visite site too frequencently
})
#hyer.event.add_event("new_document",extract_doc)
spider.run_loop(); 
