import sys
import re
sys.path.append('../')
import unittest
import hyer.browser
import hyer.event
import hyer.filter
import hyer.vendor.TextExtract
import copy
import hyer.helper
import hyer.urlfunc
global debug
debug=1

class PyFilterTest(unittest.TestCase):
    ''' ...'''
    def test_extract_links(self):
        html=open("./data/index.html").read()
        ret=hyer.urlfunc.extract_links(html)
        print ret
if __name__ == "__main__":
    unittest.main()  
		

