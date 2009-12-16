#coding:utf-8

from BeautifulSoup import BeautifulSoup
import re

R_TRIM=re.compile("<.*?>",re.M|re.S)
class NoneConfig(dict):
    def value(self):
        return None
    def __getitem__(self,key):
        return NoneConfig()

def regexp(str):
    return re.compile(str,re.M|re.S);

def list(str):
    return str.split("||")

class Config(dict):
    """ 话说一米六二同志特别懒,这个配置文件的解析,就是证明:
    这个配置文件解析类,居然就是用的BeautifulSoup来解析的,懒到家了....
    @brief
    Example:
    config=hyer.config.Config(open("./share/demo.conf").read())
    print config["root"]["db"].value()
    """
    def __init__(self,content,last_find=None):
        self.content=content
        self.last_find=last_find
        self.soup= BeautifulSoup(self.content)
        self.builders={
                "string":str,
                "regexp":regexp,
                "list":list,
                "python":eval
                }
    def __str__(self):
        return self.content

    def value(self):

        v=self.last_find.next
        #R_TRIM.sub("",self.content)
        try:
            type=self.last_find["type"]
        except:
            type="string"
        print "type:",type
        return self.builders[type](v)

    def __getitem__(self,key):
        data=self.soup.find(key)
        self.last_find=data
        if data==None:
            return NoneConfig()
        else:
            return Config(str(data),self.last_find)
