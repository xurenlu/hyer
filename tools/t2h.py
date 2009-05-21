#!/usr/bin/python
#-*- coding:utf-8 -*-

#######
# author: kz (violet.kz at gmail.com)
# date:   2008-1-22

import re
import sys


#HTML基本字符替换.
base_char_sub=((' ','&nbsp;'),\
               ('<','&lt;'),\
               ('>','&gt;'),\
               ('\t','&nbsp;&nbsp;&nbsp;&nbsp;'),\
               ('~$','')) ##这里的'~$'不是HTML基本字符,只是简单起见,处理断行的标志符.
def rules_generator(rules):
    for aRule in rules:
        search_str, sub_str = aRule
        yield lambda raw_str: re.sub(search_str, sub_str, raw_str)

#预定义格式替换.
#   标题         => [= 标题 =]
#   一级标题     => [=1= 一级标题 =]
#   二级标题     => [=A= 二级标题 =]
#   三级标题     => [=a= 三级标题 =]
#   示例代码开始 => /* ====example(1) =======
#   示例代码结束 => ====End ======= */
#   说明开始     => [=commant_start=]
#   说明结束     => [=commant_end=]
#   引用开始     => [=ref_start=]
#   引用结束     => [=ref_end=]
#   (name,regex string)
defined_format=(('title','^\s*\[==(.*)==\]$',r'<P align=center><FONT face=宋体 size=5><STRONG>\1</STRONG></FONT></P>'),\
                ('title_1','^\s*\[=1=(.*)=\]$',r'<br /><FONT size=4><STRONG>\1</STRONG></FONT><br />'),\
                ('title_2','^\s*\[=A=(.*)=\]$',r'<br /><FONT size=3><STRONG>\1</STRONG></FONT><br />'),\
                ('title_3','\s*\[=a=(.*)=\]',r'<FONT size=1><STRONG>\1</STRONG></FONT>'),\
                ('code_start',\
                '^\s*\/\*\s*={1,4}example\(\s*\d\s*\).*$',\
                r'<FIELDSET style="COLOR: #dcdcdc; BACKGROUND-COLOR: #f0f8ff" align=left><FONT face="Lucida Console" color="#000000">'),\
                ('code_end','\s*={1,4}[eE][nN][dD]=+\*\/\s*$',r'</Font></FIELDSET>'),\
                ('comment_start','^\[=comment_start=\]',r'<p align=right><FONT size=2 color="#008080">'),\
                ('comment_end','^\[=comment_end=\]',r'</FONT></p>'),\
                ('ref_start','^\[=ref_start=\]',r'<p align=left><FONT size=1 color="#0000ff">'),\
                ('ref_end','^\[=ref_end=\]',r'</FONT></p>'))


#预定义格式替换类
class txtParse:
    def __init__(self, str, def_list = defined_format, out=sys.stdout):
        self.__strs = str.split('\n')
        self.__dflist = def_list
        self.__subed_str =''
        self.__out = out
        self.__flag = 0x0000
    def default_replace(self, res, sub, string):
        s = re.sub(res, sub, string)
        return s

    def return_Br(self, raw):
        if raw.endswith('~'):
            return ''
        else:
            return '<br />'

    def feed(self):
        for origRaw in self.__strs:
            br = self.return_Br(origRaw)
            aRaw = origRaw
            for aR in rules_generator(base_char_sub):
                aRaw = aR(aRaw)
            searched_flag = False #已处理标志位
            for aFName,aFRegex,aFSub in self.__dflist:
                #print aFName,aFRegex,aFSub
                m = re.search(aFRegex, aRaw)
                if m:
                    #查找是否有指定的处理函数.
                    funObj = getattr(self, 'do_%s' % aFName,None)
                    if funObj != None:
                        self.__subed_str +=  funObj(aFRegex, aFSub, aRaw) + br + '\n'
                    else:#在没有指定处理函数时,调用默认替换函数 
                        self.__subed_str +=  self.default_replace(aFRegex, aFSub, aRaw) + br + '\n'
                    searched_flag = True # 设置已经处理标志
                    break
            # 没有匹配所有格式的情况下，原文输出
            if not searched_flag:
                self.__subed_str += aRaw + br + '\n'
        self.__subed_str = '<html><Font size=3 face="Lucida Console" color="#000000">%s</Font></html>' % self.__subed_str
        if self.__out:
            self.__out.write(self.__subed_str)

    def get_subed_str(self):
        return self.__subed_str

    def do_code_start(self, res, subs, raw):
        self.__flag = 0x0001 
        return self.default_replace(res, subs, raw)

    def do_code_end(self, res, subs, raw):
        self.__flag = self.__flag & 0x1110 
        return self.default_replace(res, subs, raw)

    def do_comment_start(self, res, subs, raw):
        self.__flag = 0x0001 
        return self.default_replace(res, subs, raw)

    def do_comment_end(self, res, subs, raw):
        self.__flag = self.__flag & 0x1110 
        return self.default_replace(res, subs, raw)
        
test_string='[==标题==]\n[=1=标题1=]\n[=A=标题=]\n/*===example(1)\n code<<>>1 \n ===end===*/'

if __name__=="__main__": 
    import sys
    import os.path
    if len(sys.argv) == 2:
        whole_str = open(sys.argv[1]).read()
        fp = open(os.path.basename(sys.argv[1]) + '.html','w')
        txtParse(str=whole_str, out=fp).feed()
        fp.close()
    else:
        print "\n txt2html.py file_name"

