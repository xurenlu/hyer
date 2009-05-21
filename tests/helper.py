import sys
import re
sys.path.append('../')
import unittest
import hyer.helper

class PyFilterTest(unittest.TestCase):
    def test_peeker(self):
        p1=hyer.helper.peeker([1,2])
        data1=[
                [9,8,7],
                [100,99,98,97]
            ]
        self.assertEqual(p1.run(data1),98)
       
        p2=hyer.helper.peeker(["t2","s22"])
        data2={
            "t1":{"s1":1,"s2":2,"s3":3},
            "t2":{"s21":1,"s22":2,"s23":3}
        }
        self.assertEqual(p2.run(data2),2) 
if __name__ == "__main__":
    unittest.main()  
		

