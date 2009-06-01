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
        filter= \
        {
            "class":hyer.filter.RegexpExtractFilter,
            "from":"html",
            "regexp":re.compile('<body[^>]*>(.*)<\/body>'),
            "matches":[
                {
                "to":"body",
                "index":hyer.helper.peeker([0])
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
    def test_tasksplitfilter(self):
        filter=\
        {
            "class":hyer.filter.RandomProxyUrlFetchFilter,
            "agent":"Mozilla/Firefox 3.1",
            "from":"url",
            "to":"html",
            "db_path":"../db/dbpath/",
            "proxies":[
                #{"http":"http://localhost:2000"},
                {"http":"http://localhost:80"}
            ]
        }
        data=\
        {
            "url":"http://www.sina.com/"
        }
        newtasks=hyer.filter.RandomProxyUrlFetchFilter(filter).run(data)
        print len(newtasks["html"])
    def test_tidyhtmlfilter(self):
        filter=\
        {
            "class":hyer.filter.IconvFilter,
            "from":"html",
            "to":"html",
            "f":"GBK",
            "t":"UTF-8"
        }
        data=\
        {
            "html":open("./data/sohu.html").read()
        }
        #print data["html"]
        output=hyer.filter.IconvFilter(filter).run(data)
        #print output["html"]
        filter=\
        {
            "class":hyer.filter.TidyHTMLFilter,
            "from":"html",
            "to":"htmls",
            "input_encoding":"utf8",
            "output_encoding":"utf8"
        }
        output=hyer.filter.TidyHTMLFilter(filter).run(output)
        #print data["htmls"]
    def test_findSoupNodes(self):
        filter=\
        {
            "class":hyer.filter.BeautifulSoupMultiNodeFilter,
            "from":"html",
            "to":"links_nodes",
            "tagname":"a",
            "attrs":{}
        }
        data=\
        {
            "url":"http://www.162cm.com/",
            "html":open("./data/index.html").read()
        }
        outputs=hyer.filter.BeautifulSoupMultiNodeFilter(filter).run(data)
        del outputs["html"]
        #print outputs
    def test_scanlinksfilter(self):
        filter=\
        {
            "class":hyer.filter.ScanLinksFilter,
            "from":"html",
            "to":"links",
            "uri_field":"url"
        }
        data=\
        {
            "url":"http://www.162cm.com/",
            "html":open("./data/index.html").read()
        }
        outputs=hyer.filter.ScanLinksFilter(filter).run(data)
        print "scan_links:"
        del outputs["html"]
        for j in outputs["links"]:
            print j

if __name__ == "__main__":
    unittest.main()  
		

