#coding:utf-8
from __future__ import with_statement 
import subprocess 
import os 
#通用的调用外部程序的函数;
def exec(args,html):
    with os.tmpfile() as temp: 
        with open(os.devnull,"w" ) as null: 
            print >>temp,html 
            temp.seek(0) 
            html=subprocess.Popen( 
            args,
            stdin=temp, 
            stderr=null, 
            stdout=subprocess.PIPE 
            ).communicate()[0] 
    return html

#调用外部tidy来修正html
def tidy(html): 
    with os.tmpfile() as temp: 
        with open(os.devnull,"w" ) as null: 
            print >>temp,html 
            temp.seek(0) 
            html=subprocess.Popen( 
            ["tidy", "-utf8","-asxhtml"], 
            stdin=temp, 
            stderr=null, 
            stdout=subprocess.PIPE 
            ).communicate()[0] 
    return html
#调用php版的取关键词的程序来取得关键词;
def gettags(data):
    cmd=["/usr/bin/php", "./bin/get_keywords.php"]
    #cmd=["ls","/"]
    with os.tmpfile() as temp:
        print >>temp,data
        temp.seek(0)
        with open(os.devnull,"w") as null:
            return subprocess.Popen(cmd, stdin=temp, stderr=null, stdout=subprocess.PIPE ).communicate()[0]

    #begin="<body>" 
    #return html[html.find(begin)+len(begin):html.rfind("</body>")].strip() 

#print tidy("<div>x<a>a") 
