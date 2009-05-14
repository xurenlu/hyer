import sys
sys.path.append('../')
import unittest
from hyer import browser,spider,document,url_saver,rules_monster,event
global debug
debug=1

class filtersTest(unittest.TestCase):
    ''' ...'''
    def test_beautifulsoupfilter(self):
        #self.assertEqual(data,[1,2,3,4,5])
        #self.assertEqual(mobile,9)
    def test_filter(self):
        #self.assertEqual(mobile,1)
  
if __name__ == "__main__":
    unittest.main()  
		
