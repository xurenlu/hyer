"""ExtMainText: Parses HTML and filters non main text parts.

http://www.elias.cn/En/ExtMainText

ExtMainText parses a HTML document, keeps only html about main text, and 
filter advertisements and common menus in document.

algorithm comes from http://www.xd-tech.com.cn/blog/article.asp?id=59

The "if __name__ == '__main__'" part of such module can be a usage sample of 
extmaintext.
Here, have some legalese:
Copyright (c) 2008, Elias Soong
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



