#!/usr/bin/python 
# -*-coding:UTF-8-*- 

#txt2htm.py 
#Author: 张沈鹏 zsp007@gmail.com 
#Update: 2006-11-10 Beta0.2 

import sys 
import re 

def htmlWrapper(content,tag,attr): 
    return "<"+tag+" "+attr+">"+content+"" 

def fontColorWrapper(content,color): 
    return htmlWrapper(content,'font','color="#'+color+'"') 

def htmHighLight(line): 
        keywords=["if","then","else","def","for","in","return","import","print","unsigned","long","int","short","include","class","void","while","const","template"] 
         
        for i in keywords: 
                keywordMatcher=re.compile(r'\b'+i+r'\b') 
                line = keywordMatcher.sub(fontColorWrapper(i,'cf0000'), line) 

                 
        return line 
     

def txt2htm(txtName): 
    txt=open(txtName) 
     
    htmlName=filename+".html" 
    htm=open(htmlName,"w") 
     
    for line in txt: 
        line=line.replace('&','&amp;')\
            .replace('<','&lt;')\
            .replace('? ','?')\
            .replace('"','&quote;')\
            .replace('?','?')\
            .replace('?','?')\
            .replace('>','&gt;')\
            .replace('\t',"    ")\
            .replace(' ',' ')

        line=""+htmHighLight(line) 

        print line 

        htm.write( line) 
         
    txt.close() 
    htm.close() 

     
    print "\n转换成功,保存在"+htmlName+'\n' 


if len(sys.argv) < 2: 
    print "\n请指定要转换为htm的文件\n" 
else: 
    filename=sys.argv[1] 
    txt2htm(filename)
