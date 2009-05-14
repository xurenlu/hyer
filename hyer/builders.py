#!/usr/bin/python
#coding:utf-8
import sys
import os
class Builder:
    def __init__(self,setting):
        self.config=setting
        self.filters=[]
        for filter in setting["filters"]:
            self.add_filter(filter)
    def add_filter(self,filter):
        self.filters.append(filter)
    def run(self,data):
        print "abstract class builder running..."

class GenericBuilder:
    def __init__(self,setting):
        self.config=setting
        self.filters=[]
        for filter in setting["filters"]:
            self.add_filter(filter)

    def _not_none(self,v):
        if v == None:
            sys.exit(1)
    def _default(self,setting,key):
        pass
    def add_filter(self,filter):
        self.filters.append(filter)
        pass
    def run(self,data):
        for filter in self.filters:
            data=filter["class"](filter).run(data)
        return True 
class FileRowsTaskBuilder(Builder):
    def run(self,data):
        initdata=data
        temp=initdata
        f=open(self.config["taskfile"],"r")
        lines=f.readlines()
        f.close
        i=0
        for line in lines:
            line=line.strip()
            temp["URI"]=line
            temp["ID"]=i
            GenericBuilder(self.config).run(temp)
            i=i+1
        return True 
class JsonFileTaskBuilder(Builder):
    def run(self,data):
        initdata=data
        temp=initdata
        f=open(self.config["taskfile"],"r")
        lines=f.readlines()
        f.close
        i=0
        for line in lines:
            line=line.strip()
            temp=json.loads(line)
            GenericBuilder(self.config).run(temp)
            i=i+1
        return True 
