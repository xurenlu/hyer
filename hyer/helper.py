#!/usr/bin/python
#coding:utf-8

import copy
def helper_trim(str,args=[]):
    return str.strip()
def helper_rtrim(str,args=[]):
    return str.rtrim()
def helper_catstr(str,args=[]):
    return "%s%s" % (str,args[0] )


class peeker:
    def __init__(self,order):
        self.order=order
    def run(self,data):
        order=copy.copy(self.order)

        #setting this to [] ,return the data himself
        if order==[]:
            return data
        order.reverse()
        running=True
        temp=copy.copy(data)
        try:
            while True:
#((key=order.pop())!=None):
                key=order.pop()
                temp=temp[key]
        except:
            pass
        return temp

