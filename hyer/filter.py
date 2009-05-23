#!/usr/bin/python
#coding:utf-8
import sys
import os
import json
from BeautifulSoup import BeautifulSoup
import re
import hyer.browser
import copy
_MAX_PAGENUM=10000
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
    {
        "class":hyer.filter.ExtractFilter,
        "from":"html",
        "to":"body",
        "starttag":"<body>",
        "endtag":"</body>"
    }
    '''
    def run(self,data):
        if isinstance(data[self.config["from"]],list):
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
        if isinstance(data[self.config["from"]],list):
            temp=[]
            startpos,endpos=(0,0)
            for frm in data[self.config["from"]]:
                temp_to={}
                startpos,endpos=(0,0)
                for tag in self.config["tags"]:#
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
    {
        "class":hyer.filter.DeleteItemFilter,
        "from":"",
        "delete_items":["html","body"],
    }
    '''
    def run(self,data):
        if (not self.config.has_key("from")) or  self.config["from"] == "":
            for v in self.config["delete_items"]:
                del data[v]
        else:
            if isinstance(data[self.config["from"]],list):
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
class UrlFetchFilter(Filter):
    '''
    fetch URL from the 'from' field and save to 'to' field
    {
        "class":hyer.filter.UrlFetchFilter,
        "agent":"Mozilla/Firefox 3.1",
        "from":"url",
        "to":"html",
        "db_path":"../db/dbpath/",
    }
    '''
    def run(self,data):
        if isinstance(data[self.config["from"]],list):
            raise ValueError("from field can't be list")
            return data
        url=data[self.config["from"]]
        browser=hyer.browser.SimpleBrowser(self.config["agent"])
        browser.setCache(self.config["db_path"]+"/cache/")
        resp=browser.getHTML(url)
        if resp==None:
            return data
        else:
            data[self.config["to"]]=resp
        return data

class XpathFilter(Filter):
    pass
class JsonDisplayFilter(Filter):
    ''' dump the data and print it for debug'''

    def  run(self,data):
        print json.dumps(data)
        return data
class DebugVarFilter(Filter):
    '''
    print specific symbols such as \n\n...
    {
        "class":hyer.filter.DebugVarFilter,
        "toprint":"\n\n"
    }
    '''
    def run(self,data):
        if self.config.has_key("toprint"):
            print self.config["toprint"]
        else:
            print "\n\n"
class DisplayFilter(Filter):
    '''
    dump the data just for debub
    {
       "class":hyer.filter.DisplayFilter
    }
    '''
    def dump(self,vr,depth):
        '''var_dump '''
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
    {
        "class":hyer.filter.ReMixArrayFilter,
        "from":"htmls",
        "to":"html_a",
        "column":"a"
    }
    before filter data:
        {
            "htmls":{"a":"dos"}
        }
    after fitler data:
        {
            "htmls":{"a":"dos":},
            "html_a":"dos"
        }
    '''
    def run(self,data):
        if not self.config.has_key("column"):
            raise KeyError("setting['column'] can't be null [ ReMixArrayFilter ]")
        if not self.config.has_key("to"):
            raise KeyError("setting['to'] can't be null [ ReMixArrayFilter ]")

        if not self.config.has_key("from"):
            towrite=data
        else:
            towrite=data[self.config["from"]]
        if isinstance(towrite,list):
            temp=[]
            for v in towrite:
                temp.append(v[self.config["column"]])
            data[self.config["to"]]=temp
        else:
            data[self.config["to"]]=towrite[self.config["column"]]
        return data
class ExitFilter(Filter):
    '''nothing but exit the filters chain.
    just for debuging .
    example:
    {
        "class":hyer.filter.ExitFilter
    }
    '''
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
        
        if isinstance(data[self.config["from"]],list):
            raise ValueError("the from parameter of hyer.filter.BeautifulSoupMultiNodeFilter can't be Array")
            return data
        
        soup=BeautifulSoup(data[self.config["from"]])
        
        results=soup.findAll(self.config["tagname"],self.config["attrs"])
        temp=[]
        for iter in results:
            temp.append(str(iter)) 
        data[self.config["to"]]=temp
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
        if isinstance(data[self.config["from"]],list):
            raise ValueError("the from parameter of hyer.filter.BeautifulSoupSingleNodeFilter can't be Array")
            return data
        
        soup=BeautifulSoup(data[self.config["from"]])
        data[self.config["to"]]=str(soup.find(self.config["tagname"],self.config["attrs"]))
        del soup
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
        if isinstance(data[self.config["from"]],list):
            temp={}
            for iter in self.config["matches"]:
                data[iter["to"]]=[] 
            for frm in data[self.config["from"]]:
                matches=[]
                matches=r.findall(frm)
                for iter in self.config["matches"]:
                    data[iter["to"]].append(iter["index"].run(matches))
            
        else:
            matches=r.findall(data[self.config["from"]])
            for iter in self.config["matches"]:
                data[iter["to"]]=iter["index"].run(matches)
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
        if isinstance(data[self.config["from"]],list):
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

class MaxPageGetterByStringFilter(Filter):
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
        "to":"maxpage" # 
    }
    '''
    def run(self,data):
        config={}
        self.retries=0
        browser=hyer.browser.SimpleBrowser(self.config["agent"])
        browser.setCache(self.config["db_path"]+"/cache/")
        if not self.config.has_key("startat"):
            self.config["startat"]=1
        if not self.config.has_key("step"):
            self.config["step"]=1
        i=self.config["startat"]
        while True:
            url = data[self.config["template"]].replace("_page_",str(i))
            url = url.replace("_step_",str(self.config["step"]))
            try:
                html=browser.getHTML(url)
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
            if i>_MAX_PAGENUM:
                return data


class ExitLoopFilter(Filter):
    '''just exit the loop'''
    def run(self,data):
        raise hyer.error.ExitLoopError("exit the loop")
class UrlListGeneratorFilter(Filter):
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
        maxpage=1
        if not self.config.has_key("maxpage"):
            maxpage=_MAX_PAGENUM
        else:
            maxpage=data[self.config["maxpage"]]
        
        while i <= maxpage:
            url = data[self.config["template"]].replace("_page_",str(i))
            url = url.replace("_step_",str(self.config["step"]))
            urllist.append(url)
            i=i+self.config["step"]
        data[self.config["to"]]=urllist
        return data

class ExtMainTextFilter(Filter):
    ''' 
        Extract Main text from HTML content
        see hyer/vendor/TextExtract.py
        {
            "class":hyer.filter.ExtMainTextFilter,
            "from":"html",
            "to":"main_text",
            "threshold":0.03
        }
    '''
    def run(self,data):
        if not self.config.has_key("from"):
            raise hyer.error.ConfigError("You must  specific [from] field")
        if not self.config.has_key("to"):
            raise hyer.error.ConfigError("You must  specific [to] field")
        if not self.config.has_key("threshold"):
            raise hyer.error.ConfigError("You must  specific [threshold] field")
        if isinstance(data[self.config["from"]],list): 
            data[self.config["to"]]=[]
            for frm in data[self.config["from"]]:
               data[self.config["to"]].append( hyer.vendor.TextExtract.extMainText(frm,self.config["threshold"])) 
        else:
            data[self.config["to"]]=hyer.vendor.TextExtract.extMainText(data[self.config["from"]],self.config["threshold"])
        return data
class Html2TextBySoupFilter(Filter):
    '''
        Extract Text data from HTML
        {
            'class':hyer.filter.Html2TextBySoupFilter,
            'from',"body",
            "to","text"
        }
    '''
    def _handle(self,html):
        '''
        return text data for 'html' variable
        '''
        #r_cmt=re.compile('<!--.+?-->')
        #r_tag=re.compile('<.*?>')
        soup = BeautifulSoup(html) 
        text = "".join(soup.findAll(text=True))
        return text
    def run(self,data):
        if isinstance(data[self.config["from"]],list):
            data[self.config["to"]]=[]
            for frm in data[self.config["from"]]:
               data[self.config["to"]].append(self._handle(frm)) 
        else:
            data[self.config["to"]]=self._handle(data[self.config["from"]])
        return data
class FuncFilter(Filter):
    '''
        Extract data by specific function
        {
            "class":hyer.filter.FuncFilter,
            "from":"string",
            "to":"len",
            "func":len
        }
    '''
    def run(self,data):
        if not self.config.has_key("func"):
            raise hyer.error.ConfigError("config['func'] can't be null")
        if isinstance(data[self.config["from"]],list):
            data[self.config["to"]]=[]
            for frm in data[self.config["from"]]:
               data[self.config["to"]].append(self.config["func"](frm)) 
        else:
            data[self.config["to"]]=self.config["func"](data[self.config["from"]])
        return data

class TaskSplitFilter(Filter):
    '''
        split task/production to lots of productions
        其实这个filter里有一个很大的不同:其他的filter虽然也是传值方式，但是是可以改变输入参数值的。这里却没有改变,输入参数啥也没改变,只是返回一堆新数组.
        {
            "class":hyer.filter.TaskSplitFilter,
            "from":"urlist",
            "to":"urlist"
        }

    '''
    def run(self,data):
        if not isinstance(data[self.config["from"]],list):
            raise hyer.error.ConfigError("config['from'] must be list ")
        
        tempdata=[]
        frm=data[self.config["from"]]
        for item in frm:
            iter=copy.copy(data)
            del iter[self.config["from"]]
            iter[self.config["to"]]=item
            tempdata.append(iter)
        return tempdata
