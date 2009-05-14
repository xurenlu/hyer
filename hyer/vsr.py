#!/usr/bin/python
#coding:utf-8
import sys
import os
import hyer.builders
class VSR:

    def __init__(self,setting):
        self.builders=setting["builders"]
    def run(self):
        for builder in self.builders:
            data=builder["data"]  #初始化数据.
            if builder.has_key("class") and builder["class"] :
                data=builder["class"](builder).run(data)
            else:
                data=hyer.builders.Builder(builder).run(data)
        pass
