#coding:utf-8
import json
class Writer:
    """filters implements function like writing to db"""
    def __init__(self,config):
        self.config=config
    def run(self,data):
        if(self.config["from"]==""):
            towrite=data
        else:
            towrite=data[self.config["from"]]
        #do some thing here...
        return data
class MySQLWriter(Writer):
    def run(self,config,data):
        pass
class ResetFileWriter(Writer):
    '''
        delete  file data["write_to"]
    '''
    def run(self,data):
        if  self.config.has_key('write_to'):
            os.unlink(self.config["write_to"])
        else:
            raise KeyError("write_to can't be null")
        return data
class TextFileWriter(Writer):
    def run(self,data):
        if(self.config["from"]==""):
            towrite=data
        else:
            towrite=data[self.config["from"]]

        if  self.config.has_key('write_to'):
            str=json.dumps(towrite)
            fl=open(self.config["write_to"],"w")
            print >>fl,str
            fl.close()
        else:
            raise KeyError("write_to can't be null")
        return data
class LineAppendWriter(Writer):
    '''
    write array items to file 
    row by row
    '''
    def run(self,data):
        if(self.config["from"]==""):
            towrite=data
        else:
            towrite=data[self.config["from"]]
        
        if  self.config.has_key('write_to'):
            if towrite.__class__ == type([]):
                mstr="\n".join(towrite)
            else:
                mstr=towrite
            #if data.has_key("__ID__"):
                #fl=open(self.config["write_to"]+str(data["__ID__"]),"w")
            #else:
            fl=open(self.config["write_to"],"a")
            print >>fl,str(mstr)
            fl.close()
        else:
            raise KeyError("write_to can't be null")
        
        return data 
class JsonLineAppendWriter(Writer):
    '''
    write array items to file 
    row by row
    '''
    def run(self,data):
        if(self.config["from"]==""):
            towrite=data
        else:
            towrite=data[self.config["from"]]

        if  self.config.has_key('write_to'):
            mstr=json.dumps(towrite)
            fl=open(self.config["write_to"],"a+")
            print >>fl,str(mstr)
            fl.close()
        else:
            raise KeyError("write_to can't be null")
        
        return data 
