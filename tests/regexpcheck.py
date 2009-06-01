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

def test_regexpcheckfilter():
    data={
            "url": "http://business.sohu.com/20090409/n263287936.shtml"
        }
    filter=\
    {
        "class":hyer.filter.RegexpCheckFilter,
        "from":"url",
        "regexp":re.compile(r'.*n[\d]+\.shtml',re.I)
    }
    print "checkExp:"
    j=filter["class"](filter).run(data)
    print j
    print "done"
		
test_regexpcheckfilter()
