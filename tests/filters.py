import sys
import re
sys.path.append('../')
import unittest
import hyer.browser
import hyer.event
import hyer.filter
global debug
debug=1

class PyEventTest(unittest.TestCase):
    ''' ...'''
    def test_event(self):
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
if __name__ == "__main__":
    unittest.main()  
		

