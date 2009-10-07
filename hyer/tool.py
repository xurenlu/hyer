#!/usr/bin/python
#coding:utf-8
import sys
import time
import pprint
import os
import json
from BeautifulSoup import BeautifulSoup
import hashlib
import re
import MySQLdb
import hyer.browser
import hyer.urlfunc
import hyer.document
import copy
import random
import hyer.vendor.TextExtract
import hyer.vendor.bloom
import hyer.singleton_bloom
import hyer.worker
_MAX_PAGENUM=100000
class Tool:
    def __init__(self,config):
        self.config=config
        pass
    def run(self,product):
        print "the class [%s] executed.\n" % self.__class__
        return product
class ExtractTool(Tool):
    '''
    Extract Data by specifying starttag and endtag
    the string between starttag and endtag is the target product
    {
        "class":hyer.tool.ExtractTool,
        "from":"html",
        "to":"body",
        "starttag":"<body>",
        "endtag":"</body>"
    }
    '''
    def run(self,product):
        if isinstance(product[self.config["from"]],list):
            temp=[]
            for frm in product[self.config["from"]]:
                startpos=frm.index(self.config["starttag"])+ len(self.config["starttag"])
                endpos=frm.index(self.config["endtag"],startpos)
                temp.append(frm[startpos:endpos])
            product[self.config["to"]]=temp 
            return product
        else:
            startpos=product[self.config["from"]].index(self.config["starttag"])+ len(self.config["starttag"])
            endpos=product[self.config["from"]].index(self.config["endtag"],startpos)
            product[self.config["to"]]=product[self.config["from"]][startpos:endpos]
            return product
class ExtractMultiFieldsTool(Tool):
    def run(self,product):
        if isinstance(product[self.config["from"]],list):
            temp=[]
            startpos,endpos=(0,0)
            for frm in product[self.config["from"]]:
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
            product[self.config["to"]]=temp 
        else:
            startpos,endpos=(0,0)
            frm=product[self.config["from"]]
            for tag in self.config["tags"]:
                startpos=frm.index(tag["starttag"],startpos)+len(tag["starttag"])
                endpos=frm.index(tag["endtag"],startpos)
                product[tag["to"]]=frm[startpos:endpos]
        return product  
class DeleteItemTool(Tool):
    '''
    delete items from hash product
    {
        "class":hyer.tool.DeleteItemTool,
        "from":"",
        "delete_items":["html","body"],
    }
    '''
    def run(self,product):
        if (not self.config.has_key("from")) or  self.config["from"] == "":
            for v in self.config["delete_items"]:
                try:
                    del product[v]
                except Exception,e:
                    raise hyer.error.IgnoreError(str(e))
        else:
            if isinstance(product[self.config["from"]],list):
                for productitem in product[self.config["from"]]:
                    for v in self.config["delete_items"]:
                        try:
                            del productitem[v]
                        except Exception,e:
                            raise hyer.error.IgnoreError(str(e))

        return product
class FormaterTool(Tool):
    '''
    @code
    {"class":hyer.tool.FormaterTool,
    "from":"id",
    "to":"url",
    "template","http://www.162cm.com/archives/%s.html"
    }
    @endcode
    '''
    def run(self,product):
        product[self.config["to"]]=self.config["template"] % product[self.config["from"]]
        return product
class MultiExtractTool(Tool):
    '''
    extract some product 
    '''
    def run(self,product):
        startpos=0
        endpos=0
        temp=[]
        try:
            while (endpos<len(product[self.config["from"]])):
                startpos=product[self.config["from"]].index(self.config["starttag"],endpos)+len(self.config["starttag"])
                endpos=product[self.config["from"]].index(self.config["endtag"],startpos)
                temp.append(product[self.config["from"]][startpos:endpos])
        except:
            pass
        product[self.config["to"]]=temp
        return product
class InfoExtractTool(Tool):
		pass
class UrlFetchTool(Tool):
    '''
    fetch URL from the 'from' field and save to 'to' field
    {
        "class":hyer.tool.UrlFetchTool,
        "agent":"Mozilla/Firefox 3.1",
        "from":"url",
        "to":"html",
        "db_path":"../db/dbpath/",
    }
    '''
    def run(self,product):
        if not self.config.has_key("db_path"):
            self.config["db_path"]="./"
        if not self.config.has_key("agent"):
            self.config["agent"]="Mozilla/Firefox 3.1 "
        if isinstance(product[self.config["from"]],list):
            raise ValueError("from field can't be list")
            return product
        url=product[self.config["from"]]
        browser=hyer.browser.Browser(self.config["agent"])
        browser.setCache(self.config["db_path"]+"/cache/")
        resp=browser.getHTML(url)
        time.sleep(0.5)
        if resp==None:
            return product
        else:
            product[self.config["to"]]=resp
        return product
class RandomProxyUrlFetchTool(Tool):
    '''
    fetch URL from the 'from' field and save to 'to' field
    {
        "class":hyer.tool.RandomProxyUrlFetchTool,
        "agent":"Mozilla/Firefox 3.1",
        "from":"url",
        "to":"html",
        "db_path":"../db/dbpath/",
        "proxies":[
            {"http":"http://localhost:2000"},
            {"http":"http://10.2.2.4:3128"}
        ]
    }
    '''
    def run(self,product):
        if isinstance(product[self.config["from"]],list):
            raise ValueError("from field can't be list")
            return product
        if not self.config.has_key("proxies"):
            raise hyer.error.ConfigError("RandomProxyUrlFetchTool must get ['proxies'] value")
        url=product[self.config["from"]]
        i=len(self.config["proxies"])
        i=random.randint(1,i)-1
        proxy=self.config["proxies"][i]
        browser=hyer.browser.Browser(self.config["agent"],proxy)
        browser.setCache(self.config["db_path"]+"/cache/")
        resp=browser.getHTML(url)
        if resp==None:
            return product
        else:
            product[self.config["to"]]=resp
        return product

class XpathTool(Tool):
    pass
class JsonDisplayTool(Tool):
    ''' dump the product and print it for debug'''

    def  run(self,product):
        print json.dumps(product)
        return product
class DebugVarTool(Tool):
    '''
    print specific symbols such as \n\n...
    {
        "class":hyer.tool.DebugVarTool,
        "toprint":"\n\n"
    }
    '''
    def run(self,product):
        if self.config.has_key("toprint"):
            print self.config["toprint"]
        else:
            print "\n\n"
        return product
class DisplayTool(Tool):
    '''
    dump the product just for debub
    {
       "class":hyer.tool.DisplayTool
    }
    '''
    def dump(self,vr,depth):
        '''var_dump '''
        print " " * depth,vr.__class__
        if isinstance(vr,list):
            i=0
            print " " * depth,"["
            for v in vr:
                i=i+1
                print " " * depth,"list item [",i,"]:"
                self.dump(v,depth+1)
            print "],"
        elif isinstance(vr,dict):
            print " " * depth,"{"
            for v in vr:
                print " " * depth," ",v,":"
                self.dump(vr[v],depth+1)
            print " " * depth,"},"
        elif isinstance(vr,str):
            if len(vr)>500:
                print " " * depth,vr[:500],","
            else:
                print " " * depth,vr,","

        else:
            print " " * depth,vr,","
    def run(self,product):
        print "[hyer.filte.DisplayTool] product:"
        pp=pprint.PrettyPrinter()
        pp.pprint ( product )
        #self.dump(product,0)
        return product
class ReMixArrayTool(Tool):
    '''
    fetch one column from rows of an array and re-generate a new array
    {
        "class":hyer.tool.ReMixArrayTool,
        "from":"htmls",
        "to":"html_a",
        "column":"a"
    }
    before tool product:
        {
            "htmls":{"a":"dos"}
        }
    after fitler product:
        {
            "htmls":{"a":"dos":},
            "html_a":"dos"
        }
    '''
    def run(self,product):
        if not self.config.has_key("column"):
            raise KeyError("setting['column'] can't be null [ ReMixArrayTool ]")
        if not self.config.has_key("to"):
            raise KeyError("setting['to'] can't be null [ ReMixArrayTool ]")

        if not self.config.has_key("from"):
            towrite=product
        else:
            towrite=product[self.config["from"]]
        if isinstance(towrite,list):
            temp=[]
            for v in towrite:
                temp.append(v[self.config["column"]])
            product[self.config["to"]]=temp
        else:
            product[self.config["to"]]=towrite[self.config["column"]]
        return product
class ExitTool(Tool):
    '''nothing but exit the tools chain.
    just for debuging .
    example:
    {
        "class":hyer.tool.ExitTool
    }
    '''
    def run(self,product):
        sys.exit(0)

class BeautifulSoupMultiNodeTool(Tool):
    """
    Extra html tag nodes by BeautifulSoup 
    example:
    {
        "class":hyer.tool.BeautifulSoupMultiNodeTool(Tool):
        "from":"html",
        "to":"links_nodes",
        "tagname":"a",
        "attrs":{"align":"center","class":re.compile("classtext .*")}
    }
    """
    def run(self,product):
        
        if isinstance(product[self.config["from"]],list):
            raise ValueError("the from parameter of hyer.tool.BeautifulSoupMultiNodeTool can't be Array")
            return product
        
        soup=BeautifulSoup(product[self.config["from"]])
        
        results=soup.findAll(self.config["tagname"],self.config["attrs"])
        temp=[]
        for iter in results:
            temp.append(str(iter)) 
        product[self.config["to"]]=temp
        #print "got %d nodes:%s " % ( len(temp),product["url"]) 
        return product
class BeautifulSoupSingleNodeTool(Tool):
    """
    Extra a single html tag node by BeautifulSoup 
    example:
    {
        "class":hyer.tool.BeautifulSoupSingleNodeTool(Tool):
        "from":"html",
        "to":"homepage_links_node",
        "tagname":"a",
        "attrs":{"align":"center","id":"main-link"}
    }
    """
    def run(self,product):
        if isinstance(product[self.config["from"]],list):
            raise ValueError("the from parameter of hyer.tool.BeautifulSoupSingleNodeTool can't be Array")
            return product
        
        soup=BeautifulSoup(product[self.config["from"]])
        product[self.config["to"]]=str(soup.find(self.config["tagname"],self.config["attrs"]))
        del soup
        return product
class RegexpExtractTool(Tool):
    """
    extrat product by regexp
    example:
    {
        "class":hyer.tool.RegexpExtractTool,
        "from":"html",
        "regexp":re.compile('(<body.*>(.*)</body>)'),
        "matches":[
            {
            "to":"body",
            "index":hyer.helper.peeker([0])
            }
            ,
            {
            "to":"body_inner",
            "index":hyer.helper.peeker([1])
            }
        ]
    }
    """
    def run(self,product):
        r=self.config["regexp"]
        if isinstance(product[self.config["from"]],list):
            temp={}
            for iter in self.config["matches"]:
                product[iter["to"]]=[] 
            for frm in product[self.config["from"]]:
                matches=[]
                matches=r.findall(frm)
                for iter in self.config["matches"]:
                    product[iter["to"]].append(iter["index"].run(matches))
            return product 
        else:
            matches=r.findall(product[self.config["from"]])
            for iter in self.config["matches"]:
                product[iter["to"]]=iter["index"].run(matches)
            return product 
class RegexpMultiExtractTool(Tool):
    """
    extrat product by regexp
    example:
    {
        "class":hyer.tool.RegexpExtractTool,
        "from":"html",
        "regexp":re.compile('(<body.*>(.*)</body>)'),
        "to":"results",
        "matches":[
            {
            "to":"body",
            "index":hyer.helper.peeker([0])
            }
            ,
            {
            "to":"body_inner",
            "index":hyer.helper.peeker([1])
            }
        ]
    }
    notes:这个跟regexpExtractTool不一样。这个是遍历所有符合条件的，把结果存入数组.返回的结果中的各项是数组.
    """
    def run(self,product):
        r=self.config["regexp"]
        if self.config["to"]==self.config["from"]:
            raise hyer.error.ConfigError("from and to fields should not be equal.")
        #product[self.config["to"]]=[]
        tempproduct=[]
        if isinstance(product[self.config["from"]],list):
            raise hyer.error.ConfigError("product['from'] can't be list"+str(product[self.config["from"]]))
            temp={}
            for iter in self.config["matches"]:
                tempproduct[iter["to"]]=[] 
            for frm in product[self.config["from"]]:
                matches=[]
                matches=r.findall(frm)
                for iter in self.config["matches"]:
                    tempproduct[iter["to"]].append(iter["index"].run(matches))
            product[self.config["to"]]=tempproduct
            return product 
        else:
            matches=r.findall(product[self.config["from"]])
            for match in matches:
                temp={}
                for iter in self.config["matches"]:
                    temp[iter["to"]]=iter["index"].run(match)
                tempproduct.append(temp)
            product[self.config["to"]]=tempproduct
            return product 
class AddStringTool(Tool):
    """add an string at the left side
    {
        "class":hyer.tool.AddStringTool,
        "from":"URI",
        "side":"right",
        "string":"page=_page_",
        "to":"newurl"
    }
    """
    def run(self,product):
        if isinstance(product[self.config["from"]],list):
            temp=[]
            for frm in product[self.config["from"]] :
                if self.config["side"]=="left":
                    temp.append( self.config["string"]+frm)
                else:
                    temp.append( frm+self.config["string"])
            product[self.config["to"]]=temp
            
        else:
            if self.config["side"]=="left":
                product[self.config["to"]]=self.config["string"]+str(product[self.config["from"]])
            else:
                product[self.config["to"]]=str( product[self.config["from"]]) +str(self.config["string"])

        return product 

class AddFieldsTool(Tool):
    """add an string at the left side
    {
        "class":hyer.tool.AddFieldsTool,
        "from":"URI",
        "side":"right",
        "add_field":"string",
        "to":"newurl"
    }
    """
    def run(self,product):
        if isinstance(product[self.config["from"]],list):
            temp=[]
            for frm in product[self.config["from"]] :
                if self.config["side"]=="left":
                    temp.append( str(product[self.config["add_field"]])+str(frm))
                else:
                    temp.append( str(frm)+str(product[self.config["add_field"]]))
            product[self.config["to"]]=temp
            
        else:
            if self.config["side"]=="left":
                product[self.config["to"]]=str(product[self.config["add_field"]])+str(product[self.config["from"]])
            else:
                product[self.config["to"]]= str(product[self.config["from"]]) +str(product[self.config["add_field"]])

        return product 

class MaxPageGetterTool(Tool):
    '''
    some list page do't specific the MAX page number.
    just with prev-page,next-page, So We find it  page and  page
    and get the right number last;
    config items:
    {
        "class":hyer.tool.MaxPageGetterTool,
        "startat":"startat",#means product['startat'] field
        "step":"step", #means product['startat'] field
        "musthave":"next page",
        "template":"http://www.162cm.com/page/_page_.html",
        "to":"maxpage", # 
        "agent":"Mozilla/Firefox",
        "db_path":"./162cm/"
    }
    '''
    def run(self,product):
        config={}
        self.retries=0
        browser=hyer.browser.SimpleBrowser(self.config["agent"])
        browser.setCache(self.config["db_path"]+"/cache/")
        startat=1
        step=1
        if self.config.has_key("startat"):
            startat=int(product[self.config["startat"]])
        if self.config.has_key("step"):
            step=int(product[self.config["step"]])
        else:
            raise hyer.error.ConfigError(" please specific config['step'] field")
            return product
        i=startat
        while True:
            url = product[self.config["template"]].replace("_page_",str(i))
            url = url.replace("_step_",str(step))
            try:
                html=browser.getHTML(url)
            except :
                #print "page number ",i," too big.."
                product[self.config["to"]]=max(i-step,1)
                return product

            if html == None:
                product[self.config["to"]]=max(i-step,1)
                #print "html is none"
                #print "page number ",i," too big.."
                return product

            try:
                pos=html.index(self.config["musthave"])
                #print " page:",i," is not max page"
            except ValueError,er:
                #print "page number ",i," too big.."
                product[self.config["to"]]=i
                return product
            i=i+step
            if i>_MAX_PAGENUM:
                product[self.config["to"]]=i
                return product

class CleverMaxpageGetterTool(Tool):
    '''
    This tool is clever enough to get the maxpage number
    This tool use MaxPageGetterByStringTool
    {
        "class":hyer.tool.CleverMaxPageGetterTool,
        "startat":"startat",
        "step":"step",
        "musthave":"next pate",
        "to":"maxpage",
        "db_path":"./",
        "template":"http://www.162cm.com/page/_page_.html",
        "agent":"Mozilla/Firefox",
    }
    '''
    def run(self,product):
        startat=int(product[self.config["startat"]])
        step=int(product[self.config["step"]])
        temp=step
        tempproduct=product
        power=11
        if self.config.has_key("power"):
            power=self.config["power"]
        #$tempproduct[self.config["to"]]=data[self.config["startat"]]
        for i in range(power,-1,-1):
            temp=step * 2 ** i
            #print "product[step]=>",temp
            product[self.config["step"]]=temp
            tempProduct=hyer.tool.MaxPageGetterTool(self.config).run(product)
            product[self.config["startat"]]=tempProduct[self.config["to"]]
            if temp==step:
                product[self.config["startat"]]=startat
                product[self.config["step"]]=step
                return product
            product[self.config["startat"]]=tempProduct[self.config["to"]]+temp/2
            #print tempproduct
        product[self.config["startat"]]=startat
        product[self.config["step"]]=step
        return product

class ExitLoopTool(Tool):
    '''just exit the loop'''
    def run(self,product):
        raise hyer.error.ExitLoopError("exit the loop")
class UrlListGeneratorTool(Tool):
    '''
    {
        "class":hyer.tool.UrlListGeneratorTool,
        "template":"url_template",
        "startat":1,
        "step":1,
        "maxpage":"max",
        "to":"urls"
    }
    '''
    def run(self,product):
        '''
        generate url list 
        '''
        urllist=[]
        startat=1
        step=1
        template=product[self.config["template"]]
        if self.config.has_key("startat"):
            startat=product[self.config["startat"]]
        if self.config.has_key("step"):
            step=product[self.config["step"]]
        i=startat
        maxpage=1
        if not self.config.has_key("maxpage"):
            maxpage=_MAX_PAGENUM
        else:
            maxpage=product[self.config["maxpage"]]
        
        while i <= maxpage:
            url = product[self.config["template"]].replace("_page_",str(i))
            url = url.replace("_step_",str(step))
            urllist.append(url)
            i=i+step
        product[self.config["to"]]=urllist
        return product

class ExtMainTextTool(Tool):
    ''' 
        Extract Main text from HTML content
        see hyer/vendor/TextExtract.py
        {
            "class":hyer.tool.ExtMainTextTool,
            "from":"html",
            "to":"main_text",
            "threshold":0.03,
            "min_length":300
        }
    '''
    def run(self,product):
        if not self.config.has_key("from"):
            raise hyer.error.ConfigError("You must  specific [from] field")
        if not self.config.has_key("to"):
            raise hyer.error.ConfigError("You must  specific [to] field")
        if not self.config.has_key("threshold"):
            raise hyer.error.ConfigError("You must  specific [threshold] field")
        if not self.config.has_key("min_length"):
            self.config["min_length"]=300
        if isinstance(product[self.config["from"]],list): 
            product[self.config["to"]]=[]
            for frm in product[self.config["from"]]:
                tmp=hyer.vendor.TextExtract.extMainText(frm,self.config["threshold"])
                if len(tmp)>self.config["min_length"]:
                    product[self.config["to"]].append( tmp) 
        else:
            tmp=hyer.vendor.TextExtract.extMainText(product[self.config["from"]],self.config["threshold"])
            if len(tmp)>self.config["min_length"]:
                product[self.config["to"]]=tmp
            else:
                raise hyer.error.ExitLoopError("can't extract main text .")
        return product
class Html2TextBySoupTool(Tool):
    '''
        Extract Text product from HTML
        {
            'class':hyer.tool.Html2TextBySoupTool,
            'from',"body",
            "to","text"
        }
    '''
    def _handle(self,html):
        '''
        return text product for 'html' variable
        '''
        #r_cmt=re.compile('<!--.+?-->')
        #r_tag=re.compile('<.*?>')
        soup = BeautifulSoup(html) 
        text = "".join(soup.findAll(text=True))
        return text
    def run(self,product):
        if isinstance(product[self.config["from"]],list):
            product[self.config["to"]]=[]
            for frm in product[self.config["from"]]:
               product[self.config["to"]].append(self._handle(frm)) 
        else:
            product[self.config["to"]]=self._handle(product[self.config["from"]])
        return product
class FuncTool(Tool):
    '''
        Extract product by specific function
        {
            "class":hyer.tool.FuncTool,
            "from":"string",
            "to":"len",
            "func":len
        }
    '''
    def run(self,product):
        if not self.config.has_key("func"):
            raise hyer.error.ConfigError("config['func'] can't be null")
        if isinstance(product[self.config["from"]],list):
            product[self.config["to"]]=[]
            for frm in product[self.config["from"]]:
               product[self.config["to"]].append(self.config["func"](frm)) 
        else:
            product[self.config["to"]]=self.config["func"](product[self.config["from"]])
        return product

class StringSplitTool(Tool):
    '''
    将一个字符串按特定字符切分成数组.
    如果refill指定为yes,则数组的第二项，第三项...第n项会再把SP加到最前面.
    {
        "class":hyer.tool.StringSplitTool,
        "SP":"<br>",
        "refill":"yes",
        "from":"html",
        "to":"paragraphes"
    }
    '''
    def run(self,product):
        temp=product[self.config["from"]].split(self.config["SP"])  
        if self.config["refill"]=="yes":
            temp2=[]
            j=0
            for iter in temp:
                if j>0:
                    temp2.append(self.config["SP"]+iter)
                else:
                    temp2.append(iter)
                j=j+1
        else:
            temp2=temp
        product[self.config["to"]]=temp2
        return product 

class TaskSplitTool(Tool):
    '''
        split task/production to lots of productions
        其实这个tool里有一个很大的不同:其他的tool虽然也是传值方式，但是是可以改变输入参数值的。这里却没有改变,输入参数啥也没改变,只是返回一堆新数组.
        {
            "class":hyer.tool.TaskSplitTool,
            "from":"urlist",
            "to":"urlist",
            "new_product_id_from":None #默认值。黙认情况下会用原来的__PRODUCT_ID__ 加整数.
        }

    '''
    def run(self,product):
        if not isinstance(product[self.config["from"]],list):
            raise hyer.error.ConfigError("config['from'] must be list ")
        if not self.config.has_key("new_product_id_from"):
            self.config["new_product_id_from"]=None

        tempproduct=[]
        frm=product[self.config["from"]]
        k=0
        for item in frm:
            k=k+1
            iter=copy.copy(product)
            del iter[self.config["from"]]
            iter[self.config["to"]]=item
            if self.config["new_product_id_from"]==None:
                key=product["__PRODUCT_ID__"]+":"+str(k)
            elif isinstance(self.config["new_product_id_from"],list):
                key=""
                sp=""
                try:
                    for i in self.config["new_product_id_from"]:
                        key = key + str(iter[i])+sp
                        sp=":"
                except Exception,e:
                    print "exception when generation new product_id,",e,e.__class__
                    pass
            else:
                key=self.config["new_product_id_from"].run(item)

            #限定最长product_id为32位.
            if len(key)<32:
                iter["__PRODUCT_ID__"]=key
            else:
                iter["__PRODUCT_ID__"]=hashlib.md5(key).hexdigest()
            tempproduct.append(iter)
        return tempproduct
class ScanLinksTool(Tool):
    '''
    从[from]扫描出所有链接,再利用[uri_field]拼接出完整的地址.
    {
        "class":hyer.tool.ScanLinksTool,
        "from":"html",
        "uri_field":"URI",
        "to":"links",
        "validate_url_regexps":[ re.compile('http:\/\/business\.sohu\.com\/'), re.compile('http:\/\/money\.sohu\.com')]
    }
    '''
    def run(self,product):
        frm=product[self.config["from"]]
        url=product[self.config["uri_field"]]
        base_dir=hyer.urlfunc.get_base(frm,url)
        links=[]
        all_original_links=hyer.urlfunc.extract_links(frm)
        #print "got all_original_links"
        #print all_original_links
        all_original_links=hyer.urlfunc.remove_bad_links(all_original_links)
        urls=[]
        hrefs=[]
        for l in all_original_links: 
            u=hyer.urlfunc.get_full_url(l["url"],base_dir)
            u=hyer.urlfunc.fix_url(u)
            if self.validate_url(u):
                if not u in hrefs:
                    urls.append({"url":u,"text":l["text"]})
                    hrefs.append(u)
        #print "got  %d links from %s" % ( len(urls),url )
        product[self.config["to"]]=urls
        return product
    def validate_url(self,u):
        '''check if the url need to be visited,
            generelly removing pictures,css and javascript files
            and if the param conf (specified when you initing the object) set leave_domain false,fire this valida
        '''
        #如果定义了same_domain_regexps,
        #就必须检查.
        if self.config.has_key("validate_url_regexps"):
            validate_url=False
            for validate_url_regexp in self.config["validate_url_regexps"]:
                if validate_url_regexp.match(u):
                    validate_url=True
            if validate_url==False:
                return False
            else:
                return True
        else:
            return True

class TidyHTMLTool(Tool):
    '''
    用tidy 来对某个html进行检查修正.
    仅限UTF-8
    utidylib的主页:
    http://pypi.python.org/pypi/uTidylib/0.2
    {
        "class":hyer.tool.TidyHTMLTool,
        "from":"html",
        "to":"html",
        "input_encoding":"utf8",
        "output_encoding":"UTF8"
    }
    '''
    def run(self,product):
        '''
        '''
        import tidy
        frm=product[self.config["from"]]
        try:
            input_enc=self.config["input_encoding"]
        except:
            input_enc="utf8"
        try:
            output_enc=self.config["output_encoding"]
        except:
            output_enc="utf8"
        try:
            if isinstance(frm,list):
                outputs=[]
                for it in frm:
                    outputs.append(str(tidy.parseString(it,
                    input_encoding=input_enc,
                    output_encoding=output_enc,
                    preserve_entities="yes",
                    accessibility_check=0,
                    new_empty_tags="",
                    output_html="yes",
                    show_errors=6,
                    force_output="yes"

                        )))
                product[self.config["to"]]=outputs
            else:
                product[self.config["to"]]=str(tidy.parseString(frm,
                    input_encoding=input_enc,
                    output_encoding=output_enc,
                    preserve_entities="yes",
                    accessibility_check=0,
                    new_empty_tags="",
                    output_html="yes",
                    show_errors=6,
                    force_output="yes"
                    ))
        except Exception,e:
            print "got an exception when tidy...",e
        return product

class IconvTool(Tool):
    '''convert product to other encoding:
    {
        "class":hyer.tool.IconvTool,
        "f":"GBK",
        "t":"UTF-8",
        "from":"html",
        "to":"html"
    }
    '''
    def run(self,product):
        if not self.config.has_key("f"):
            raise hyer.error.ConfigError("config[f] can't be null")
        if not self.config.has_key("t"):
            raise hyer.error.ConfigError("config[t] can't be null")

        frm=product[self.config["from"]]
        if isinstance(frm,list):
            outputs=[]
            for it in frm:
                outputs.append( it.decode(self.config["f"],"ignore").encode(self.config["t"],"ignore"))
            product[self.config["to"]]=outputs
        else:
            product[self.config["to"]]= frm.decode(self.config["f"],"ignore").encode(self.config["t"],"ignore")
        return product
class UniqueCheckTool(Tool):
    '''
    check if an unique key is exists ,
    and if exists, just exit the loop
    {
        "class":hyer.tool.UniqueCheckTool,
        "from":"url"
    }
    '''
    def run(self,product):
        if isinstance(product[self.config["from"]],list):
            raise hyer.error.ConfigError("product['from'] can't be list")
        frm=product[self.config["from"]]
        if hyer.singleton_bloom.exists(frm):
            print "exit the loop because UniqueCheckTool:" + str(frm)
            raise hyer.error.ExitLoopError("exit the loop because UniqueCheckTool:" + str(frm))
        else:
            hyer.singleton_bloom.add(frm)
        return product

class RegexpCheckTool(Tool):
    '''
    check if the specific field matches the regexp
    if not,raise a hyer.error.ExitLoopError
    {
        "class":hyer.tool.RegexpCheckTool,
        "regexp":re.compile('.*n[\d]+\.shtml',re.I),
        "from":"url"
    }
    '''
    def run(self,product):
        if isinstance(product[self.config["from"]],list):
            raise hyer.error.ConfigError("product[from] can't be list")
        if not self.config["regexp"].match(product[self.config["from"]]):
           raise hyer.error.ExitLoopError("product[%s] not match re." % self.config["from"])
        return product

class ValueCheckTool(Tool):
    '''
    if some filed of product equals specific value, exitloop
    {
        "class":hyer.tool.ValueCheckTool,
        "field":hyer.helper.peeker(["value"]),
        "value":[]
    }
    means :if product['value']==[]:
                raise ExitLoopError('...')
    '''
    def run(self,product):
        if self.config["field"].run(product)== self.config["value"]:
            raise hyer.error.ExitLoopError("ValueCheckTool exitloop")
        return product

class DirectSetTool(Tool):
    '''
    just set some field of the product
    {
        "class":hyer.tool.DirectSetTool,
        "to":"text",
        "value":"这是一个标题",
    }
    '''
    def run(self,product):
        product[self.config["to"]]=self.config["value"]
        return product

class FixProductIdTool(Tool):
    '''
    {
        'class':hyer.tool.FixProductIdTool,
        "from":hyer.helper.peeker([]),
        "seed":"url"
    }
    '''

class FetchAndFixTool(Tool):
    '''
    {
        "class":hyer.tool.FetchAndFixTool,
        "from":"url",
        "to":"html",
        "encoding":"utf-8",
    },
    '''
    def run(self,product):
        if not self.config.has_key("db_path"):
            self.config["db_path"]="./"
        if not self.config.has_key("agent"):
            self.config["agent"]="Mozilla/Firefox 3.1 "
        if not self.config.has_key("encoding"):
            self.config["encoding"]="UTF-8"

        #print "goto fetch:",product["url"]
        tools= \
            [
                {
                    "class":hyer.tool.UniqueCheckTool,
                    "from":"url",
                },
                {
                    "class":hyer.tool.UrlFetchTool,
                    "to":"html",
                    "agent":self.config["agent"],
                    "from":"url",
                    "db_path":self.config["db_path"]
                },
                {
                    "class":hyer.tool.IconvTool,
                    "f":self.config["encoding"],
                    "t":"UTF-8",
                    "from":"html",
                    "to":"html"
                },
                {
                    "class":hyer.tool.TidyHTMLTool,
                    "from":"html",
                    "to":"html",
                    "input_encoding":"utf8",
                    "output_encoding":"utf8"
                }
            ]
        worker=hyer.worker.Worker()
        worker.tools=tools
        worker.post="innercalled"
        tempProduct=worker.process(product)
        for key in tempProduct:
            product[key]=tempProduct[key]
        return product
        #comment
class CopyTool(Tool):
    '''
    copy some field to other field
    {
        "class":hyer.tool.CopyTool,
        "from":hyer.helper.peeker([1,"url"]),
        "to":"url"
    }
    '''
    def run(self,product):
        '''
        '''
        source=self.config["from"].run(product)
        product[self.config["to"]]=source
        return product
class JoinTool(Tool):
    '''
    Join list as String
    {
        "class":hyer.tool.JoinTool,
        "from":hyer.helper.peeker([1,"url"]),
        "to":"url",
        "SP":""
    }
    '''
    def run(self,product):
        '''
        '''
        if not self.config.has_key("SP"):
            self.config["SP"]=""
        source=self.config["from"].run(product)
        if not isinstance(source,list):
            product[self.config["to"]]=source
        else:
            product[self.config["to"]]=self.config["SP"].join(source)
        return product

class ReplaceTool(Tool):
    '''
    replace some chars to other chars
    {
        "class":hyer.tool.ReplaceTool,
        "from":hyer.helper.peeker(["from"])
        "to":"url",
        "replace_from":" "
        "replace_to":"%20"
    }
    '''
    def run(self,product):
        source=self.config["from"].run(product)
        product[self.config["to"]]=source.replace(self.config["replace_from"],self.config["replace_to"])
        return product

class Sleeper(Tool):
    def run(self,product):
        time.sleep(self.config['time'])
        return product

class MysqlFetcher(Tool):
    def run(self,product):
        '''
        取回某个worker线程要完成的工作
        '''
        try:
            print(self.config)
            self.conn=MySQLdb.connect(self.config["host"],self.config["user"],self.config["pass"],self.config["db"])
            self.cursor=self.conn.cursor(MySQLdb.cursors.DictCursor)
            self.cursor.execute("set names utf8")
            self.cursor.execute(self.config["sql"])
            rows=self.cursor.fetchall()
            j=0
            returns=[]
            for row in rows:
                j+=1
                if self.config.has_key("new_product_id_from"):
                    row["__PRODUCT_ID__"]=str(row[self.config["new_product_id_from"]])
                else:
                    row["__PRODUCT_ID__"]=str(j)
                returns.append(row)
            return returns
        except Exception,e:
            print "error from mysqlfetcher:",e.__class__,e
            hyer.log.track()
            pass
        return None

