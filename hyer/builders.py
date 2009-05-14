#!/usr/bin/python
#coding:utf-8
import sys
import os
import hyer.error
class Builder:
    def __init__(self,setting):
        '''
        A builder has a source and many filters;
        builder run loops :pop up from source,sent to filters,and fetch the data,sent to filters....
        and try to write to db by a dbwriter filter'''
        self.config=setting
        self.filters=[]
        for filter in setting["filters"]:
            self.add_filter(filter)
        self.source=setting["source"]["class"](setting["source"])

    def add_filter(self,filter):
        self.filters.append(filter)
    def single_run(self,data):
        pass
    def run(self,data):
        print "abstract class builder running..."

class GenericBuilder(Builder):

    def _not_none(self,v):
        if v == None:
            sys.exit(1)
    def _default(self,setting,key):
        pass
    def add_filter(self,filter):
        self.filters.append(filter)
        pass
    def run(self,data):
        #while(temp=self.source.pop()):
        self.source.init(data)
        while(True):
            temp=self.source.pop()
            if temp == None:
                return data
            data["__ITER__"]=temp
            for filter in self.filters:
                try:
                    data=filter["class"](filter).run(data)
                except hyer.error.ExitLoopError,e:
                    return False
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
            temp["__ROW__"]=line
            temp["__ID__"]=i
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
