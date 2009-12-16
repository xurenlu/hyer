#coding:utf-8

from BeautifulSoup import BeautifulSoup
import re

R_TRIM=re.compile("<.*?>",re.M|re.S)
class NoneConfig(dict):
    def value(self):
        return None
    def __getitem__(self,key):
        return NoneConfig()

class Config(dict):
    """ 话说一米六二同志特别懒,这个配置文件的解析,就是证明:
    这个配置文件解析类,居然就是用的BeautifulSoup来解析的,懒到家了....
    @brief
    Example:
    config=hyer.config.Config(open("./share/demo.conf").read())
    print config["root"]["db"].value()
    """
    def __init__(self,content):
        self.content=content
        self.soup= BeautifulSoup(self.content)

    def __str__(self):
        return self.content

    def value(self):
        return R_TRIM.sub('',self.content)
    def __getitem__(self,key):
        data=self.soup.find(key)
        if data==None:
            return NoneConfig()
        else:
            return Config(str(data))
