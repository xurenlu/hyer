import sys
sys.path.append('../')
import unittest
from hyer import browser,spider,document,url_saver
import hyer.document
import hyer.spider
import hyer.url_saver
import hyer.browser
import hyer.rules_monster
class UrlSaver(unittest.TestCase):
	def test_pop(self):
		us=url_saver.url_saver()
		us.add("http://www.sina.com/","task1")
		us.add("http://www.sohu.com/","task1")
		url=us.pop("task1")
		#self.assertEqual(url,"http://www.sohu.com/")	
		url=us.pop("task2")
		#self.assertEqual(url,"http://www.sina.com/")	
		us.mark("http://www.sina.com/","task1")
		if_visited=us.if_visited("http://www.sina.com/","task1")
		self.assertEqual(if_visited,1)
		if_visited=us.if_visited("http://www.sohu.com/","task1")
		self.assertEqual(if_visited,0)
class SpiderText(unittest.TestCase):
	def stest_fix_url(self):
		sp=spider.spider([])
		self.assertEqual(sp.fix_url("http://www.sohu.com/../i/fin/./../index*.html"),"http://www.sohu.com/i/index2A%.html")
	def stest_get_dir(self):
		sp=spider.spider([])
		self.assertEqual(sp.get_dir("http://www.sohu.com/index.html"),"http://www.sohu.com/")
		self.assertEqual(sp.get_dir("http://www.sohu.com/i/ndex.html"),"http://www.sohu.com/i/")
		self.assertEqual(sp.get_dir("http://www.sohu.com"),"http://www.sohu.com/")
		self.assertEqual(sp.get_dir("http://www.sohu.com/"),"http://www.sohu.com/")
	def stest_get_domain_seg(self):
		sp=spider.spider([])
		self.assertEqual(sp.get_domain_seg("http://www.sina.com/dos.html"),"http://www.sina.com")	
		self.assertEqual(sp.get_domain_seg("http://www.sina.com/"),"http://www.sina.com")	
		self.assertEqual(sp.get_domain_seg("http://www.sina.com"),"http://www.sina.com")	
	def stest_get_base_dir(self):
		sp=spider.spider([])
		file="search.html"
		s=open(file,"r").read()
		doc=(document.HTMLDocument(s))
		self.assertEqual(sp.get_base_dir(doc,"http://www.spider.com/dsfdsf/html.html"),"http://www.spider.com/dsfdsf/")

		file="search2.html"
		s=open(file,"r").read()
		doc=(document.HTMLDocument(s))
		self.assertEqual(sp.get_base_dir(doc,"http://www.spider.com/dsfdsf/html.html"),"http://www.sina.com/dos/")
	def stest_get_full_url(self):
		sp=spider.spider([])
		self.assertEqual(sp.get_full_url("http://www.sohu.com/dos.html","http://localhost/sina.com/"),"http://www.sohu.com/dos.html")
		self.assertEqual(sp.get_full_url("/tes.html","http://www.sina.com/tes/"),"http://www.sina.com/tes.html")
		self.assertEqual(sp.get_full_url("tess.html","http://www.sina.com/dos/"),"http://www.sina.com/dos/tess.html")
	def test_save_doc(self):
		sp=hyer.spider.spider({"task":"newtask","feed":"http://localhost/search_doc/web/perl/","leave_domain":None,"same_domain_regexp":r'http:\/\/localhost\/search_doc\/web\/perl',"agent":"Hyer/0.5.4 (http://www.162cm.com/","db_path":"data/","buckets":32})
		f=open("search.html","r")
		html=f.read()
		f.close()
		u="file:///search.html"
		doc=document.HTMLDocument(html,u)
		sp.save_document(doc,u,"./data/")
if __name__ == "__main__":
    unittest.main()  
