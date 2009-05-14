#!/usr/bin/python
#coding:utf-8
import sys
import os
import json
from BeautifulSoup import BeautifulSoup
import re
class Filter:
    def __init__(self,config):
        self.config=config
        pass
    def run(self,data):
        print "the class [%s] executed.\n" % self.__class__
        return data
class ExtractFilter(Filter):
    '''
    Extract Data by specifying starttag and endtag
    the string between starttag and endtag is the target data
    '''
    def run(self,data):
        if data[self.config["from"]].__class__==type([]):
            temp=[]
            for frm in data[self.config["from"]]:
                startpos=frm.index(self.config["starttag"])+ len(self.config["starttag"])
                endpos=frm.index(self.config["endtag"],startpos)
                temp.append(frm[startpos:endpos])
            data[self.config["to"]]=temp 
            return data
        else:
            startpos=data[self.config["from"]].index(self.config["starttag"])+ len(self.config["starttag"])
            endpos=data[self.config["from"]].index(self.config["endtag"],startpos)
            data[self.config["to"]]=data[self.config["from"]][startpos:endpos]
            return data
class ExtractMultiFieldsFilter(Filter):
    def run(self,data):
        if data[self.config["from"]].__class__== type([]):
            temp=[]
            startpos,endpos=(0,0)
            for frm in data[self.config["from"]]:#遍历各个from字段..
                temp_to={}
                startpos,endpos=(0,0)
                for tag in self.config["tags"]:#遍历各个tags
                    try:
                        startpos=frm.index(tag["starttag"],startpos)+len(tag["starttag"])
                        endpos=frm.index(tag["endtag"],startpos)
                        temp_to[tag["to"]]=frm[startpos:endpos]
                        endpos=endpos+len(tag["endtag"])
                        startpos=endpos
                    except ValueError,e:
                        print "error,substring failed:from:",frm,"\n,start:",startpos,"\n,end",endpos,"\n,starttag",tag["starttag"],"\nendtag:",tag["endtag"],"\nto:",tag["to"]
                        pass
                temp.append(temp_to) 
            data[self.config["to"]]=temp 
        else:
            startpos,endpos=(0,0)
            frm=data[self.config["from"]]
            for tag in self.config["tags"]:
                startpos=frm.index(tag["starttag"],startpos)+len(tag["starttag"])
                endpos=frm.index(tag["endtag"],startpos)
                data[tag["to"]]=frm[startpos:endpos]
        return data  
class DeleteItemFilter(Filter):
    '''
    delete items from hash data
    '''
    def run(self,data):
        if self.config["from"] == "":
            for v in self.config["delete_items"]:
                del data[v]
        else:
            if data[self.config["from"]].__class__ == type([]):
                for dataitem in data[self.config["from"]]:
                    for v in self.config["delete_items"]:
                        del dataitem[v]
        return data
class FormaterFilter(Filter):
    '''
    @code
    {"class":hyer.filter.FormaterFilter,
    "from":"id",
    "to":"url",
    "template","http://www.162cm.com/archives/%s.html"
    }
    @endcode
    '''
    def run(self,data):
        data[self.config["to"]]=self.config["template"] % data[self.config["from"]]
        return data
class MultiExtractFilter(Filter):
    '''
    extract some data 
    '''
    def run(self,data):
        startpos=0
        endpos=0
        temp=[]
        try:
            while (endpos<len(data[self.config["from"]])):
                startpos=data[self.config["from"]].index(self.config["starttag"],endpos)+len(self.config["starttag"])
                endpos=data[self.config["from"]].index(self.config["endtag"],startpos)
                temp.append(data[self.config["from"]][startpos:endpos])
        except:
            pass
        data[self.config["to"]]=temp
        return data
class InfoExtractFilter(Filter):
		pass
class RegexpFilter(Filter):
    pass
class UrlFilter(Filter):
    pass
class XpathFilter(Filter):
    pass
class JsonDisplayFilter(Filter):
    ''' dump the data and print it for debug'''

    def  run(self,data):
        print json.dumps(data)
        return data
class DisplayFilter(Filter):
    '''
    dump the data just for debub
    '''
    def dump(self,vr,depth):
        '''var_dump 变量'''
        if vr.__class__ == type([]):
            i=0
            print " " * depth,"["
            for v in vr:
                i=i+1
                print " " * depth,"list item [",i,"]:"
                self.dump(v,depth+1)
            print "],"
        elif vr.__class__ == type({}):
            print " " * depth,"{"
            for v in vr:
                print " " * depth," ",v,":"
                self.dump(vr[v],depth+1)
            print " " * depth,"},"

        else:
            print " " * depth,vr,","
    def run(self,data):
        print "data:"
        self.dump(data,0)
        return data
class ReMixArrayFilter(Filter):
    '''
    fetch one column from rows of an array and re-generate a new array
    '''
    def run(self,data):
        if not self.config.has_key("column"):
            raise KeyError("setting['from'] can't be null [ ReMixArrayFilter ]")
        if not self.config.has_key("to"):
            raise KeyError("setting['to'] can't be null [ ReMixArrayFilter ]")

        if not self.config.has_key("from"):
            towrite=data
        else:
            towrite=data[self.config["from"]]

        if towrite.__class__ == type([])    :
            temp=[]
            for v in towrite:
                temp.append(v[self.config["column"]])
            data[self.config["to"]]=temp
        else:
            data[self.config["to"]]=towrite[self.config["column"]]
        return data
class ExitFilter(Filter):
    '''nothing but exit the filters chain.
    just for debuging .'''
    def run(self,data):
        sys.exit(0)

class BeautifulSoupMultiNodeFilter(Filter):
    """
    Extra html tag nodes by BeautifulSoup 
    example:
    {
        "class":hyer.filter.BeautifulSoupMultiNodeFilter(Filter):
        "from":"html",
        "to":"links_nodes",
        "tagname":"a",
        "attrs":{"align":"center","class":re.compile("classtext .*")}
    }
    """
    def run(self,data):
        if data[self.config["from"]].__class__ == type([]):
            raise ValueError("the from parameter of hyer.filter.BeautifulSoupMultiNodeFilter can't be Array")
            return data
        
        soup=BeautifulSoup(data[self.config["from"]])
        data[self.config["to"]]=soup.findAll(self.config["tagname"],self.config["attrs"])
        return data
class BeautifulSoupSingleNodeFilter(Filter):
    """
    Extra a single html tag node by BeautifulSoup 
    example:
    {
        "class":hyer.filter.BeautifulSoupSingleNodeFilter(Filter):
        "from":"html",
        "to":"homepage_links_node",
        "tagname":"a",
        "attrs":{"align":"center","id":"main-link"}
    }
    """
    def run(self,data):
        if data[self.config["from"]].__class__ == type([]):
            raise ValueError("the from parameter of hyer.filter.BeautifulSoupSingleNodeFilter can't be Array")
            return data
        
        soup=BeautifulSoup(data[self.config["from"]])
        data[self.config["to"]]=soup.find(self.config["tagname"],self.config["attrs"])
        return data
class RegexpExtractFilter(Filter):
    """
    extrat data by regexp
    example:
    {
        "class":hyer.filter.RegexpExtractFilter,
        "from":"html",
        "regexp":re.compile('(<body.*>(.*)</body>)'),
        "matches":[
            {
            "to":"body",
            "index":0
            }
            ,
            {
            "to":"body_inner",
            "index":1
            }
        ]
    }
    """
    def run(self,data):
        r=self.config["regexp"]
        if data[self.config["from"]].__class__ == type([]):
            temp={}
            for iter in self.config["matches"]:
                temp[iter["to"]]=[] 
            for frm in data[self.config["from"]]:
                matches=[]
                matches=r.findall(frm)
                for iter in self.config["matches"]:
                    temp[iter["to"]].append(matches[iter["index"]])
        else:
            #单个源字符串的处理..
            matches=r.findall(data[self.config["from"])
            data[self.config["to"]]=matches[
            for iter in self.config["matches"]:
                data[iter["to"]]=matches[iter["index"]]
            return data 
class AddStringFilter(Filter):
    """add an string at the left side
    {
        "class":hyer.filter.AddStringFilter,
        "from":"URI",
        "side":"right",
        "string":"page=_page_",
    }
    """
    def run(self,data):
        if data[self.config["from"]].__class__ == type([]):
            temp=[]
            for frm in data[self.config["from"]] :
                if self.config["side"]=="left":
                    temp.append( self.config["string"]+frm)
                else:
                    temp.append( frm+self.config["string"])
            data[self.config["to"]]=temp
            
        else:
            if self.config["side"]=="left":
                data[self.config["to"]]=self.config["string"]+data[self.config["from"]]
            else:
                data[self.config["to"]]= data[self.config["from"]] +self.config["string"]

        return data 
