#coding:utf-8
import json
import hyer.error
import hyer.tinySQL
import MySQLdb
class Writer:
    """tools implements function like writing to db"""
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
    '''
    {
        "class":hyer.dbwriter.MySQLWriter,
        "fields":["ranktype","page","nodeid","bookid","ord"],
        "host":configure["host"],
        "user":configure["user"],
        "pass":configure["pass"],
        "db":configure["db"],
        "table":"ranks2",
        "insert_method":"insert" # or replace
    }
    '''
    def run(self,data):
        if not self.config.has_key("host"):
            raise hyer.error.ConfigError("MysqlWriter need config['host'] filed")
            return data
        if not self.config.has_key("user"):
            raise hyer.error.ConfigError("MysqWriter need config['user'] filed")
            return data
        if not self.config.has_key("db"):
            raise hyer.error.ConfigError("MysqWriter need config['db'] filed")
            return data
        if not self.config.has_key("pass"):
            raise hyer.error.ConfigError("MysqWriter need config['pass'] filed")
            return data
        if not self.config.has_key("table"):
            raise hyer.error.ConfigError("MysqWriter need config['table'] filed")
            return data
        if not self.config.has_key("fields"):
            raise hyer.error.ConfigError("MysqWriter need config['fields'] filed")
            return data
        if not self.config.has_key("insert_method"):
            self.config["insert_method"]="insert"

        if self.config.has_key("from"):
            if self.config["from"]=="":
                frm=data
            else:
                frm=data[self.config["from"]]
        else:
            frm=data
        dict={}
        for f in self.config["fields"]:
            dict[f]=frm[f]
        sql=hyer.tinySQL.create(self.config["table"],dict,self.config["insert_method"])
        conn=MySQLdb.connect(self.config["host"],self.config["user"],self.config["pass"],self.config["db"])
        cursor=conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("set names utf8")
        cursor.execute(sql)
        return data
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

    {
        "class":hyer.dbwriter.LineAppendWriter,
        "from":"somefield",
        "write_to":"/var/data/dbfile",
    }
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

    {
        "class":hyer.dbwriter.JsonLineAppendWriter,
        "from":"somefield",
        "write_to":"/var/data/dbfile",
    }
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
