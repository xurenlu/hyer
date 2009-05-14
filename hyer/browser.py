# -*- coding: utf-8 -*-
import os, cookielib, urllib2,sys
import hyer.error
import socket
import hyer.diskhash
#from urlparse import urlparse
socket.setdefaulttimeout(10)
class browser:
    """ This is a browser class fetch urls for you """
    def __init__(self,user_agent="Mozilla/Firefox 3.1(http://www.firefox.com/)",cookie_file="/tmp/_hyer.browser.cookie.txt",range=204800):
            ''' create browser object'''
            self.user_agent=user_agent
            self.cookie_file=cookie_file
            self.range=range
            self.use_cache=False
            self.cache_dir=""

    def setCache(self,cache_dir="/tmp/cachedir/"):
            self.use_cache=True
            self.cache_dir=cache_dir
    def get(self,url):
        ''' get url from web site
            @param user_agent: the User-Agent segment
            '''
        url=url.strip()
        cj = cookielib.MozillaCookieJar()
        #sys.exit(0)
        try:
            cj.load(self.cookie_file)
        except:
            pass
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders= [('User-Agent',self.user_agent),('Range',"bytes=0-%d" % self.range)]
        try:
            stream=opener.open(url)
            return stream
        except urllib2.HTTPError,e:
            raise hyer.error.HTTPError("can't download URL:%s" % url)
        except StandardError,ev:
            print "error:",ev,":",url
            pass
        cj.save(self.cookie_file)
        return None

    def getHTML(self,url):
        '''
        fetch it to cache'''
        if self.use_cache:
            content=hyer.diskhash.hash_read(url,self.cache_dir)
            if not content==None:
                return content
        try:
            resp=self.get(url)
            if resp==None:
                return None
            else:
                str=resp.read()
                hyer.diskhash.hash_write(url,str,self.cache_dir)
                return str
        except hyer.error.HTTPError,er:
            raise
            return None
#        except StandardError,e:
#            print "error:",e
#            return None
class SimpleBrowser(browser):
    def get(self,url):
        #print "url",url
        #print url.__class__
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return response
