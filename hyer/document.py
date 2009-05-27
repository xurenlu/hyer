# -*- coding: utf-8 -*-
"""
Documents handling here
"""
import re
class Document(dict):
	"""parents of all document classes """
	def __init__(self,content,uri=""):
		self["URI"]=uri
		self["html"]=content
		self["links"]=[]
		self["base"]=""
		self["keywords"]=""
		self["description"]=""
		self["charset"]=""
		self["head_data"]=""
		self["title"]=""
		self["body"]=""
	def links(self):
		self['links']	

class SimpleHTMLDocument(Document):
	""" """
	href_regexs=[\
		r'href\s*=\s*[\'\"]?([+:%\/\?~=&;\\\(\),._a-zA-Z0-9-]*)(#[.a-zA-Z0-9-]*)?[\'\" ]?(\s*rel\s*=\s*[\'\"]?(nofollow)[\'\"]?)?',\
		r'(frame[^>]*src[[:blank:]]*)=[[:blank:]]*[\'\"]?(([[a-z]{3,5}:\/\/(([.a-zA-Z0-9-])+(:[0-9]+)*))*([+:%\/?=&;\\\(\),._ a-zA-Z0-9-]*))(#[.a-zA-Z0-9-]*)?[\'\" ]?',\
		r'(window[.]location)[[:blank:]]*=[[:blank:]]*[\'\"]?(([[a-z]{3,5}:\/\/(([.a-zA-Z0-9-])+(:[0-9]+)*))*([+:%\/?=&;\\\(\),._ a-zA-Z0-9-]*))(#[.a-zA-Z0-9-]*)?[\'\" ]?',\
		r"/(http-equiv=['\"]refresh['\"] *content=['\"][0-9]+;url)[[:blank:]]*=[[:blank:]]*[\'\"]?(([[a-z]{3,5}:\/\/(([.a-zA-Z0-9-])+(:[0-9]+)*))*([+:%\/?=&;\\\(\),._ a-zA-Z0-9-]*))(#[.a-zA-Z0-9-]*)?[\'\" ]?/i",\
		r'/(window[.]open[[:blank:]]*[(])[[:blank:]]*[\'\"]+(([[a-z]{3,5}:\/\/(([.a-zA-Z0-9-])+(:[0-9]+)*))*([+:%\/?=&;\\\(\),._ a-zA-Z0-9-]*))(#[.a-zA-Z0-9-]*)?[\'\" ]?/i'\
	]
	PIC_RATE=100
	HUB_RATE=20
	TYPE_TEXT=0
	TYPE_HUB=1
	TYPE_PIC=2
	def __init__(self,content,uri=""):
		""" 
		@param content:the HTML content
		@param uri:the URI of the html like file:///temp/os.html or http://www.162cm.com/index.html """
		Document.__init__(self,content)
		self["URI"]=uri
		self["html"]=content
		self["links"]=[]
		self["base"]=""
		self["keywords"]=""
		self["description"]=""
		self["charset"]=""
		self["head_data"]=""
		self["title"]=""
		self["body"]=""
		
		self.scan_links(content)
		self.parse_document_type(self["body"])
	def scan_links(self,content):
		"""return all links in the html content
		have not been validated """
		hrefs=[]
		for r in self.href_regexs:
			reg=re.compile(r)
			links=reg.findall(content)
			hrefs.extend([l[0] for l in links if l !=""])
		uniq_hrefs=list(set(hrefs))
		self['links']=uniq_hrefs
		
	def get_head_data(self,content):
		"""return <head>*</head> data in the html content"""
		try:
			r=re.compile(r'<head[^>]*>(.*?)<\/head>',re.MULTILINE|re.S)
			heads=r.findall(content)
			last_head=heads.pop()
			self["head_data"]=last_head
			return last_head
		except:
			pass
	def get_title_data(self,head):
		"""return <title>*</title> data in <head>*</head> section
		Arguments:
			-head	the <head>*</head> section content"""
		try:
			r=re.compile(r'<title[^>]*>(.*?)<\/title>',re.MULTILINE|re.S)
			titles=r.findall(head)
			title=titles.pop()
			self["title"]=title
			return title
		except:
			pass 
	def get_keywords_meta(self,head):
		"""return <meta name='keyword' data in the head content"""
		"""Get the keywords meta data of the HTML document"""
		try:
			r=re.compile("<meta +name *=[\"']?keywords[\"']? *content=[\"']?([^<>'\"]+)[\"']?",re.M|re.S)
			matches=r.findall(head)
			self["keywords"]=matches.pop()
		except:
			pass
	def get_description_meta(self,head):
		""" return description meta data in the head content"""
		try:
			r=re.compile("<meta +name *=[\"']?description[\"']? *content=[\"']?([^<>'\"]+)[\"']?",re.M|re.S)
			matches=r.findall(head)
			self["description"]=matches.pop()
		except:
			pass
	def get_robots_meta(self,head):
		"""Get the robots segment of the head"""
	def get_base_meta(self,head):
		"""get the base link meta of the head"""
		try:
			r=re.compile("<base +href *= *[\"']?([^<>'\"]+)[\"']?",re.M|re.I)
			matches=r.findall(head)
			self["base"]=matches.pop()
		except:
			pass
	def get_charset_meta(self,head):
		"""get the charset of document from the HTML head segment """
		try:
			r=re.compile("<meta +http\-equiv*=[\"']?Content-Type[\"']? *content=[\"']?([^<>'\"]+)[\"']?",re.M|re.S)
			matches=r.findall(head)
			charset_str=matches.pop().split("=").pop()
			self["charset"]=charset_str
			return charset_str
		except:
			pass
	def get_body_data(self,html):
		"""get the html between <body> and </body> tags"""
		try:
			r=re.compile("<body.*?>(.*?)</body>",re.M|re.S)
			matches=r.findall(html)
			self["body"]=matches.pop()
		except:
			pass
	def _html2text(self,text):
		"""remove html tags"""
		try:
			r=re.compile("<script[^>]*>.*?</script>",re.I|re.S)
			text=r.sub("",text)
		except:
			pass
	
		try:
			r=re.compile("<style[^>]*>.*?</style>",re.M|re.I|re.S)
			text=r.sub("",text)
		except:
			pass


		try:
			r=re.compile("<.*?>",re.M|re.S)
			text=r.sub('',text)
			return text
		except:
			pass		

	def textualize(self,body):
		"""return the text without html tags"""
		text=body
		self["text"]=self._html2text(text)
	def parse_document_type(self,html):
		"""return the document type:hub,text,pic
		hub:document with many links ,little text and pics
		text:a document with lots of words
		pics:a document focus on pictures"""
		pics=0
		links=0
		words=0
		try:
			r=re.compile("<img +",re.M|re.S)
			matches=r.findall(html)	
			pics=len(matches)
		except:
			pass
		text=self["body"]
		links=len(self["links"])
		#得到所有的非链接文字"
		words=len(text)		
		try:
			r=re.compile("<a[^>]*>.*?</a>",re.M|re.I|re.S)
			unlinked_text=r.sub("",text)
			unlinked_text=self._html2text(unlinked_text)
			words=len(unlinked_text)
		except :
			pass
		self["links_count"]=links
		self["pics_count"]=pics
		self["words_count"]=words
		self["doc_type"]=self.TYPE_TEXT
		r1=words/(pics+1)
		r2=words/(links+1)
		if r1 < self.PIC_RATE:
			self["doc_type"]=self.TYPE_PIC
		if r2 < self.HUB_RATE:
			self["doc_type"]=self.TYPE_HUB
	def parse_headers():
		pass
	def links(self):
		self['links']	


class HTMLDocument(SimpleHTMLDocument):
    def __init__(self,content,uri=''):
		""" 
		@param content:the HTML content
		@param uri:the URI of the html like file:///temp/os.html or http://www.162cm.com/index.html """
		Document.__init__(self,content)
		self["URI"]=uri
		self["html"]=content
		self["links"]=[]
		self["base"]=""
		self["keywords"]=""
		self["description"]=""
		self["charset"]=""
		self["head_data"]=""
		self["title"]=""
		self["body"]=""
		
		self.scan_links(content)
		self.get_head_data(content)
		self.get_title_data(self["head_data"])
		self.get_keywords_meta(self["head_data"])
		self.get_charset_meta(self["head_data"])
		self.get_base_meta(self["head_data"])
		self.get_description_meta(self["head_data"])
		self.get_body_data(content)
		self.textualize(self["body"])
		self.parse_document_type(self["body"])
class RSSDocument(Document):
	def __init__(self,content):
		Document.__init__(self)
	def links(self):
		self['links']	
class RSSItemDocument(Document):
	def __init__(self,content):
		Document.__init__(self)
	def links(self):
		self['links']	


