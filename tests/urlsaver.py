import sys
sys.path.append('../')
import unittest
from hyer import browser,spider,document,url_saver,rules_monster
global debug
debug=1
class UrlSaver(unittest.TestCase):
	''' ...'''
	def test_save(self):
		''' test if the url saver works as expected'''
		url_db=url_saver.url_saver()
		url_db.add("http://www.sohu.com/","task1")
		url_db.add("http://www.sina.com/2008/","task1")
		url_db.add("http://2008.sina.com/","task1")
		url_db.save_to("/tmp/_hyer.test.1954")
		b_urls_queue=url_db.urls_queue
		b_visited_urls=url_db.visited_urls
		url_db.load_from("/tmp/_hyer.test.1954")
		self.assertEqual(b_urls_queue,url_db.urls_queue)
		self.assertEqual(b_visited_urls,url_db.visited_urls)
	def test_pop(self):
		url_db=url_saver.url_saver()
		url_db.add("http://www.sohu.com/","task1")
		url_db.add("http://www.sina.com/2008/","task1")
		#self.assertEqual("http://www.sina.com/2008/",url_db.pop("task1"))	
if __name__ == "__main__":
    unittest.main()  
		
