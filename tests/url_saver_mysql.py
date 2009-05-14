import sys
sys.path.append('../')
import unittest
from hyer import browser,spider,document,url_saver_mysql,rules_monster
global debug
debug=1
class UrlSaver(unittest.TestCase):
    ''' ...'''
    def test_save(self):
        ''' test if the url saver works as expected'''
        url_db=url_saver_mysql.url_saver_mysql("localhost",8090)
        url_db.add("http://www.sohu.com/","task3")
        self.assertEqual(url_db.pop("task3"),"http://www.sohu.com/")
    def test_mark_error(self):
        url_db=url_saver_mysql.url_saver_mysql("localhost",8090)
        url_db.add("http://www.sohu.com/1.html","task4")
        url_db.add("http://www.sohu.com/2.html","task4")
        url_db.mark_error("http://www.sohu.com/1.html","task4")
        self.assertEqual(url_db.pop("task4"),"http://www.sohu.com/2.html")
    def teest_mark_visited(self):
        url_db=url_saver_mysql.url_saver_mysql("localhost",8090)
        url_db.add("http://www.sohu.com/3.html","task5")
        url_db.add("http://www.sohu.com/4.html","task5")
        url_db.mark_error("http://www.sohu.com/2.html","task5")
        url_db.mark_visited("http://www.sohu.com/3.html","task5")
        self.assertEqual(url_db.pop("task5"),"http://www.sohu.com/4.html")
        #self.assertEqual("http://www.sina.com/2008/",url_db.pop("task1"))  
if __name__ == "__main__":
    unittest.main()  
        
