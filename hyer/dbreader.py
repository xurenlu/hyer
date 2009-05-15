#coding:utf-8
import json

class Dbreader:
    '''
    read some data from files.
    this class is just an abstract class [ something called interface in java or other language]
    '''
    def __init__(self,config):
        self.config=config
    def run(self,data):
        pass


class LinesToListDbReader(Dbreader):
    '''
    read files row by row
    and save rows to   list
    {
        "class":hyer.dbreader.LinesToListDbReader,
        "readfrom":"/var/data/amazon/catenames.db",
        "to":"catenames"
    }
    '''
    def run(self,data):
        if not self.config.has_key("readfrom"):
            raise ConfigError("readfrom field of LinesToListDbReader can't be null")
        fd=open(self.config["readfrom"],"r")
        data[self.config["to"]]=[]
        lines=fd.readlines()
        fd.close() 
        for line in lines:
            line=line.strip() 
            data[self.config["to"]].append(line)
        return data
