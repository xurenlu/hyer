#!/usr/bin/python
#coding:utf-8

def helper_trim(str,args=[]):
    return str.strip()

def helper_rtrim(str,args=[]):
    return str.rtrim(str)
def helper_catstr(str,args=[]):
    return "%s%s" % (str,args[0] )


