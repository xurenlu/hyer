#coding:utf-8
import json
class Writer:
    def __init__(self,setting):
        self.setting=setting
    def run(self,data):
        if(self.setting["from"]==""):
            towrite=data
        else:
            towrite=data[self.setting["from"]]
        #do some thing here...
        return data
class MySQLWriter(Writer):
    def run(self,setting,data):
        pass
class ResetFileWriter(Writer):
    def run(self,data):
        if  self.setting.has_key('write_to'):
            os.unlink(self.setting["write_to"])
        else:
            raise KeyError("write_to can't be null")
        return data
class TextFileWriter(Writer):
    def run(self,data):
        if(self.setting["from"]==""):
            towrite=data
        else:
            towrite=data[self.setting["from"]]

        if  self.setting.has_key('write_to'):
            str=json.dumps(towrite)
            fl=open(self.setting["write_to"],"w")
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
        if(self.setting["from"]==""):
            towrite=data
        else:
            towrite=data[self.setting["from"]]

        if  self.setting.has_key('write_to'):
            if towrite.__class__ == type([]):
                mstr="\n".join(towrite)
            else:
                mstr=towrite
            if data.has_key("ID"):
                fl=open(self.setting["write_to"]+str(data["ID"]),"w")
            else:
                fl=open(self.setting["write_to"],"w")
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
        if(self.setting["from"]==""):
            towrite=data
        else:
            towrite=data[self.setting["from"]]

        if  self.setting.has_key('write_to'):
            mstr=json.dumps(towrite)
            fl=open(self.setting["write_to"],"a+")
            print >>fl,str(mstr)
            fl.close()
        else:
            raise KeyError("write_to can't be null")
        
        return data 
