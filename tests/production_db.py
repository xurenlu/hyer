#coding:utf-8
import sys
sys.path.append('../')
import unittest
import hyer.production_db
global debug
debug=1

class productionDbTest(unittest.TestCase):
    ''' ...'''
    def test_production_db(self):
        print "hi"
        pdb=hyer.production_db.ProductionDb({
            "host":"localhost",
            "db":"hyer",
            "user":"root",
            "pass":"",
            "table":"products"
        })
        p=pdb.popProduct("TextGrabber")
        print p
if __name__ == "__main__":
    unittest.main()  
		

