# -*- coding: utf-8 -*-
import time
from urlparse import urlparse
class site_holder:
    def __init__(self,domain,max_in_minute):
        '''initialization of the class
            @param domain:the domain of the site'''
        self.max_in_minute=max_in_minute
        self.domain=domain
        self.visites={}
        pass
    def visited(self,times=1):
        '''browser visites the site,so log it
            '''
        t=int(time.time())
        if self.visites.has_key(t):
            self.visites[t]=self.visites[t]+times
        else: 
            self.visites[t]=times
    def can_visit(self):
        '''if the browser can visit the site'''
        t=int(time.time())
        min=t-60
        sum=0
        visites=self.visites.copy() #copy a new value.Other wise when we delete an item when iterating ,System will throw an exception
        for k in visites:
            if (k<min):
                del self.visites[k]
            else:
                sum=sum+visites[k]
        if  (sum>self.max_in_minute):
            return False
        else:
            return True     
class site_holder_monster:
    def __init__(self,max_in_minute):
        '''initialize object'''
        self.holders={}
        self.max_in_minute=max_in_minute
        
    def visited(self,url,times=1):
        '''browser visited an url,logged the visiting
        @param url:the url just visited
        '''
		uri=urlparse(url)
        host=uri.hostname
        if self.holders.has_key(host):
            self.holders[host].visited(times)
        else:
            self.holders[host]=site_hoder(host,self.max_in_minute)
    def can_visit(self,url):
        '''if the browser can visit the url
        @param url:the url we try to visit'''
		uri=urlparse(url)
        host=uri.hostname
        if self.holders.has_key(host):
            return self.holders[host].can_visit()
        else:
            self.holders[host]=site_holder(host,self.max_in_minute)
            return True 
