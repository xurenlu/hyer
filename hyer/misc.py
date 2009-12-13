#coding:utf-8
from __future__ import with_statement 
import subprocess 
import os 
import string
from random import Random
#通用的调用外部程序的函数;

def cmd25(args,html):
    """在2.5中适用的方式"""
    cmd=string.join(args)
    (stdin,stdout)=os.popen2(cmd)
    print >>stdin,html
    out=string.join(stdout.readlines(),"\n")
    stdin.close()
    stdout.close()
    return out
def cmd(args,html):
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
def cmdmy(args,html):
    """2.5的os.popen,2.6的subprocess都有问题,所以我只好自己写一个"""
    cmd=string.join(args)
    filen="/tmp/tmp.hyer.%d" % Random().randint(100000,1000000)
    fileno=open(filen,"w+")
    print >>fileno,html
    fileno.close()
    cmd=cmd % filen
    pp=os.popen(cmd,"r")
    lines=pp.readlines()
    ret=string.join(lines ,"\n")
    os.unlink(filen)
    return ret
def tidy(html): 
    """#调用外部tidy来修正html"""
    args= ["/usr/bin/tidy", "-utf8","-asxhtml"," %s"," 2>/dev/null"]
    return cmdmy(args,html)

def gettags(data):
    """调用php版的取关键词的程序来取得关键词;"""
    cmd=["/usr/bin/php", "./bin/get_keywords.php","-f %s","2>/dev/null"]
    return cmdmy(cmd,data)
    #begin="<body>" 
    #return html[html.find(begin)+len(begin):html.rfind("</body>")].strip() 

#print tidy("<div>x<a>a") 
