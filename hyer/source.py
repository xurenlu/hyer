#coding:utf-8
import hyer.browser
import sys
import os
import time
class Source:
    def __init__(self,config):
        self.browser=hyer.browser.SimpleBrowser(config["agent"])
        self.config=config
        self.browser.setCache(config["db_path"]+"/cache/")
        self.feeds=[]
    def run(self):
        pass
    def get(self,url):
        pass
    def pop(self):
        print "pop called" #hack by renlu
        print self.feeds
        return self.feeds.pop()
    def run(self,data={}):
        pass
    def init(self,data):
        print "init function called" #hack by renlu
        if data[self.config["from"]].__class__ == type([]):
            self.feeds=data[self.config["from"]]
        else:
            self.feeds.append(data[self.config["from"]])
class Generic(Source):
    pass
class Mysql(Source):
    pass 
class UrlListGenerator(Source):
    def run(self,data):
        '''
        generate url list 
        '''
        urllist=[]
        template=data[self.config["template"]]
        if not self.config.has_key("startat"):
            self.config["startat"]=1
        if not self.config.has_key("step"):
            self.config["step"]=1
        i=self.config["startat"]
        while True:
            url = data[self.config["template"]].replace("_page_",str(i))
            url = url.replace("_step_",str(self.config["step"]))
            urllist.append(url)
        data[self.config["to"]]=urllist
        return data
