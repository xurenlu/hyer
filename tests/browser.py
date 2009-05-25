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
global debug
debug=1

class PyFilterTest(unittest.TestCase):
    ''' ...'''
    def test_regexpfiltertext(self):
        data={}
        j=hyer.browser.Browser("Mozilla/Firefox",{"http":"http://localhost:80"})
        print j.getHTML("http://www.sohu.com/")
if __name__ == "__main__":
    unittest.main()  
		


