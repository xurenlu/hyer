import sys
sys.path.append('../')
import unittest
#from hyer import browser,spider,document,url_saver,rules_monster,event
import hyer.vendor.bloom
import hyer.singleton_bloom
global debug
debug=1

class filtersTest(unittest.TestCase):
    ''' ...'''
    def test_bloom(self):
        print "hi"
        self.assertEqual( hyer.singleton_bloom.exists("good"),False)
        self.assertEqual( hyer.singleton_bloom.add("good"),None)
        self.assertEqual( hyer.singleton_bloom.exists("good"),True)
if __name__ == "__main__":
    unittest.main()  
		
