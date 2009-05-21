import sys
import re
sys.path.append('../')
import unittest
import hyer.browser
import hyer.event
import hyer.filter
import hyer.vendor.TextExtract
global debug
debug=1

class PyFilterTest(unittest.TestCase):
    ''' ...'''
    def test_regexpfiltertext(self):
        data={}
        filter= \
        {
            "class":hyer.filter.RegexpExtractFilter,
            "from":"html",
            "regexp":re.compile('<body[^>]*>(.*)<\/body>'),
            "matches":[
                {
                "to":"body",
                "index":0
                }
            ]
        }
        data={
            "html":"<html><body><div>godo</div></body></html>"
        }
        data=hyer.filter.RegexpExtractFilter(filter).run(data)
        self.assertEqual(data["body"],"<div>godo</div>")
    def test_extmaintext(self):
        data={}
        filter= \
        {
            "class":hyer.filter.ExtMainTextFilter,
            "from":"html",
            "to":"text",
            "threshold":0.03
        }
        data={ }
        j=open("data/index.html","r")
        html=j.read()
        j.close()
        data["html"]=html 
        hyer.filter.ExtMainTextFilter(filter).run(data)
#        print data["text"]
        #self.assertEqual(data["body"],"<div>godo</div>")
    def test_html2text_regexp(self):
        pass
    def test_html2text_soup(self):
        filter=\
        {
            "from":"html",
            "to":"text"
        }
        data={}
        j=open("data/index.html","r")
        html=j.read()
        j.close()
        data["html"]=html 
        hyer.filter.Html2TextBySoupFilter(filter).run(data)
    def test_funcfilter(self):
        filter=\
        {
            "from":"html",
            "to":"len",
            "func":len
        }
        data={}
        data["html"]="testdone"
        hyer.filter.FuncFilter(filter).run(data)
        self.assertEqual(data["len"],8)
        
if __name__ == "__main__":
    unittest.main()  
		

