#!/usr/bin/python
#coding:utf-8
#Author:renlu.xu
#URL:http://www.162cm.com/
#date:2009.05.21

import MySQLdb

def escape(st):
    return MySQLdb.escape_string(str(st))

def update(table,columns,condition=None):
    if isinstance(columns,dict):
        sql="UPDATE `%s` SET " % table
        comm=""
        for col in columns:
            sql = sql + comm+ "`"+col+"`='"+escape(columns[col])+"' "
            comm=","
        if condition:
            sql = sql + "WHERE " + condition
        return sql
    else:
        return None

def create(table,columns):
    if isinstance(columns,dict):
        sql="INSERT INTO `%s` (" % table
        comm=""
        for col in columns:
            sql = sql + comm + "`"+col+"`"
            comm=","
        sql = sql + ") VALUES ("
        comm=""
        for col in columns:
            sql = sql + comm + "'"+escape(columns[col])+"'"
            comm=","
        sql = sql + ")" 
        return sql
    else:
        return None
def testfunc():
    table="mytable"
    columns={
        "id":1,
        "name":"xuren'lu"
    }
    condition="id=2"
    print update(table,columns,condition)
    print create(table,columns)

if __name__=="__main__":
    testfunc()
