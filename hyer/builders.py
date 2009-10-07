#!/usr/bin/python
#coding:utf-8
import sys
import os
import hyer.error
class Builder:
    def __init__(self,setting):
        '''
        A builder has a source and many tools;
        builder run loops :pop up from source,sent to tools,and fetch the data,sent to tools....
        and try to write to db by a dbwriter tool'''
        self.config=setting
        self.tools=[]
        for tool in setting["tools"]:
            self.add_tool(tool)
        self.source=setting["source"]["class"](setting["source"])

    def add_tool(self,tool):
        self.tools.append(tool)
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
    def add_tool(self,tool):
        self.tools.append(tool)
        pass
    def run(self,data):
        self.source.init(data)
        while(True):
            try:
                temp=self.source.pop()
            except Exception,e:
                print e 
                return data
            if temp == None:
                return data
            data["__ITER__"]=temp
            for tool in self.tools:
                try:
                    tool["class"](tool).run(data)
                except hyer.error.ExitLoopError,e:
                    print "error caught:",e
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
