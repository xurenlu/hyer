# -*- coding: utf-8 -*-
import cPickle as pickle
import random
import MySQLdb
import socket  
class Urldb:
    '''class hold on urls that visited all would be visited'''
    urls_queue=[]
    visited_urls=[]
    def add(self,url,task):
        '''we found a new url and save it in the queue'''   
        index=-1
        try:
            index=self.urls_queue.index(url)
        except:
            pass
        index2=-1
        try:
            index2=self.visited_urls.index(url)
        except:
            pass
        if index==-1 and index2==-1:
            self.urls_queue.append(url)
        else:
            pass
    def pop(self,task):
        '''return an url unvisited'''
        i=random.randint(0,len(self.urls_queue)-1)
        return self.urls_queue[i]
    def mark_visited(self,url,task):
        '''
        alias as self.mark
        '''
        self.mark(url,task)
    def mark(self,url,task):
        '''mark an url as visited'''
        try:
            self.urls_queue.remove(url)
        except:
            pass

        index=-1
        try:
            index=self.visited_urls.index(url)
        except:
            pass
        if index==-1:
            self.visited_urls.append(url)
    def if_visited(self,url,task):
        ''' query if an url is visited'''
        index=-1
        try:
            index=self.visited_urls.index(url)
        except:
            pass
        if index==-1:
            return 0
        else:
            return 1        
    def save_to(self,file):
        ''' save the urls to db file'''
        try:
            data={"visited_urls":self.visited_urls,"urls_queue":self.urls_queue}
            str=pickle.dumps(data)
            f=open(file,"w")
            f.write(str)
            f.close()
        except :    
            return None
    def load_from(self,file):
        ''' load data from file'''
        try:
            f=open(file,"r")
            str=f.read()
            f.close()
            data=pickle.loads(str)
            self.urls_queue=data["urls_queue"]
            self.visited_urls=data["visited_urls"]
        except:
            return None 
    def mark_error(self,url,task):
        ''' mark an url as invalid'''
        self.mark(url,task)
    def debug(self):
        '''just for debuging'''
        print "visited_urls",self.visited_urls
        print "unvisited:",self.urls_queue
class Urldb_mysql:
    '''class hold on urls that visited all would be visited'''
    def __init__(self):
        '''initize the mysqldb connection'''
        self.conn=MySQLdb.connect('localhost','root','842519','hyer')
        self.cursor=self.conn.cursor(MySQLdb.cursors.DictCursor)
    def add(self,url,task):
        '''we found a new url and save it in the queue'''   
        index=-1
        sql="INSERT INTO urls (`url`,`task`,`status`) VALUES ('%s','%s','%s')"

        try:
            sql="INSERT INTO urls (`url`,`task`,`status`) VALUES ('%s','%s','%s')" %(url,task,'new')
            self.cursor.execute(sql)
        except Exception,e:
            pass
    def pop(self,task):
        '''return an url unvisited'''
        sql="SELECT url FROM urls WHERE status='new' AND task='%s'  LIMIT 1" % task
        #param=(task)
        n=self.cursor.execute(sql)
        rows=self.cursor.fetchall()
        if len(rows) == 0:
            return None
        return rows[0]["url"] 
    def mark(self,url,task):
        '''mark an url as visited'''
        try:
            self.urls_queue.remove(url)
        except:
            pass

        index=-1
        sql="UPDATE urls set status='visited' WHERE URL='%s' AND task='%s' " % (url,task)
        n=self.cursor.execute(sql)
#        try:
#            index=self.visited_urls.index(url)
#        except:
#            pass
#        if index==-1:
#            self.visited_urls.append(url)
    def mark_visited(self,url,task):
        self.mark(url,task)
    def if_visited(self,url,task):
        ''' query if an url is visited'''
        index=-1
        try:
            index=self.visited_urls.index(url)
        except:
            pass
        if index==-1:
            return 0
        else:
            return 1        
    def save_to(self,file):
        ''' save the urls to db file'''
        try:
            data={"visited_urls":self.visited_urls,"urls_queue":self.urls_queue}
            str=pickle.dumps(data)
            f=open(file,"w")
            f.write(str)
            f.close()
        except :    
            return None
    def load_from(self,file):
        ''' load data from file'''
        try:
            f=open(file,"r")
            str=f.read()
            f.close()
            data=pickle.loads(str)
            self.urls_queue=data["urls_queue"]
            self.visited_urls=data["visited_urls"]
        except:
            return None 
    def mark_error(self,url,task):
        ''' mark an url as invalid'''
        #self.mark(url,task)
        sql="UPDATE urls set status='error' WHERE URL='%s' AND task='%s' " % (url,task)
        n=self.cursor.execute(sql)
    def debug(self):
        '''just for debuging'''
        print "visited_urls",self.visited_urls
        print "unvisited:",self.urls_queue
class urldb_sock:
    '''class hold on urls that visited all would be visited'''
    sock=None
    host="localhsot"
    port=8089 
    
    def __init__(self,host,port):
        '''初始化连接'''
        self.host=host
        self.port=port
    def getResponse(self,msg):
        '''返回服务端的连接'''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.sock.connect((self.host,self.port))  
        self.sock.send(msg)
        ret=self.sock.recv(1024)
        self.sock.close()
        return ret
    def close(self):
        '''关闭连接'''
        self.sock.close()
    def add(self,url,task):
        '''we found a new url and save it in the queue'''   
        return self.getResponse("add %s %s" % (url,task))
    def pop(self,task):
        '''return an url unvisited'''
        return self.getResponse("pop %s " % (task))
    def mark_visited(self,url,task):
        '''mark an url as visited'''
        return self.getResponse("mark_visited %s %s" % (url,task))
    def if_visited(self,url,task):
        ''' query if an url is visited'''
        return self.getResponse("if_visited %s %s" % (url,task))
    def mark_error(self,url,task):
        '''将一条URL标记为访问出错'''
        return self.getResponse("mark_error %s %s" % (url,task))
        
