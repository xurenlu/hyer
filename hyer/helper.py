#!/usr/bin/python
#coding:utf-8

import copy
import urllib
def helper_trim(str,args=[]):
    return str.strip()
def helper_rtrim(str,args=[]):
    return str.rtrim()
def helper_catstr(str,args=[]):
    return "%s%s" % (str,args[0] )
def helper_urlencode(str,args=[]):
    return urllib.urlencode({"":str})

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
                try:
                    key=order.pop()
                except:
                    return temp
                temp=temp[key]
        except Exception,e:
            print "while hyer.helper.peeker:",e,"[",key,"]"
            pass
        return temp

