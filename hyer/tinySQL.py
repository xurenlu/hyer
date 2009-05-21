#!/usr/bin/python
#coding:utf-8
#Author:renlu.xu
#URL:http://www.162cm.com/
#date:2009.05.21

def escape(st):
    return st
def update(table,columns,condition=None):
    if isinstance(columns,dict):
        sql="UPDATE %s SET " % table
        comm=""
        for col in columns:
            sql = sql + comm+ "`"+col+"`='"+str(escape(columns[col]))+"' "
            comm=","
        if condition:
            sql = sql + "WHERE " + condition
        return sql
    else:
        return None


def testfunc():
    table="mytable"
    columns={
        "id":1,
        "name":"xurenlu"
    }
    condition="id=2"
    print update(table,columns,condition)

if __name__=="__main__":
    testfunc()
