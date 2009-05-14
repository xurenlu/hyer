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
    def run(self):
        pass
    def get(self,url):
        pass
    def pop(self):
        pass
    def run(self,data={}):
        pass
    def fetch(self,url):
        resp=self.browser.getHTML(url)
        return resp 
class Generic(Source):
    def __init__(self,config):
        self.feeds=[config["feed"]]
        self.browser=hyer.browser.SimpleBrowser(config["agent"])
        self.config=config
        self.browser.setCache(config["db_path"]+"/cache/")

    def pop(self):
        return self.feeds.pop();
    def run(self,data={}):
        url=self.pop()
        resp=self.browser.get(url)
        if resp == None:
            data["html"]=""
        else:
            data["html"]=resp.read()
        return data
class MaxPageGetterByString(Source):
    '''
    some list page do't specific the MAX page number.
    just with prev-page,next-page, So We find it  page and  page
    and get the right number last;
    config items:
    {
        "startat":1,
        "step":1,
        "musthave":"next page",
        "template:"http://www.162cm.com/archives/%s.html",
        "to":"maxpage" #存到这个字段里.save maxpage to this filed;
    }
    '''
    def run(self,data):
        config={}
        self.retries=0
        if not self.config.has_key("startat"):
            self.config["startat"]=1
        if not self.config.has_key("step"):
            self.config["step"]=1
        i=self.config["startat"]
        while True:
            url = data[self.config["template"]].replace("_page_",str(i))
            url = url.replace("_step_",str(self.config["step"]))
            try:
                html=self.fetch(url)
            except hyer.error.HTTPError,er:
                if self.retries < 3 :
                    time.sleep(5)
                    self.retries = self.retries + 1
                    continue
                else:
                    print "retry too many  times"
                    data[self.config["to"]]=max(i-1,1)
                    return data
            if html == None:
                data[self.config["to"]]=max(i-1,1)
                print "html is none"
                return data

            try:
                pos=html.index(self.config["musthave"])

            except ValueError,er:
                data[self.config["to"]]=i
                return data
            i=i+self.config["step"]
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
