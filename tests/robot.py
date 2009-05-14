import sys
sys.path.append('../')
import unittest
from hyer import browser,spider,document,url_saver,rules_monster
global debug
debug=1
class RobotParser(unittest.TestCase):
	''' ...'''
	def test_parse(self):
		from robotparser import RobotFileParser
		rules=RobotFileParser()
		rules.set_url("http://www.sogou.com/robots.txt")
		rules.read()
		self.assertEqual(rules.can_fetch("mozilla","http://www.sogou.com/sohu/robots.txt"),False)
	def test_rules_monster(self):
		rm=rules_monster.rules_monster("Rspider/1.0 (http://www.162cm.com/+)")
		self.assertEqual(rm.can_fetch("http://www.sogou.com/sohu/1.html"),False)
		self.assertEqual(rm.can_fetch("http://www.sogou.com/help/1.html"),True)
		self.assertEqual(rm.can_fetch("http://www.google.com/searchhistory/a.html"),True)
		self.assertEqual(rm.can_fetch("http://www.google.com/u/a.html"),False)
		
if __name__ == "__main__":
    unittest.main()  

