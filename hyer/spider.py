import cPickle as pickle
import re
import hyer.browser
import hyer.document
import hyer.urldb
import hyer.error
import hyer.site_holder
import hyer.urlfunc
import hyer.event
import zlib,hashlib,os
import time
import logging
import sys
import hashlib
from urlparse import urlparse
class spider:
    '''this is the main entrance of the whole library'''
    def __init__(self,conf):
        '''@param conf:a list describe the cralwer task'''

        #init the logging service
        logger = logging.getLogger()
        #logfile="_log%d" % time.time()
        logfile="hyer.log"
        hdlr = logging.FileHandler(conf["db_path"]+"/"+logfile)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.NOTSET)
        self.logger=logger
        self.logger.info("Program started")
        self.procid=0
        del hdlr
        del formatter
        del logger

        #init site_holder
        self.site_holder_monster=hyer.site_holder.site_holder_monster(conf["max_in_minute"])  
        self.conf=conf
        self.timer=1
        self.rm=hyer.rules_monster.rules_monster(conf["agent"])
        self.same_domain_regexps=conf["same_domain_regexps"]
        try:
            if conf["task"]:
                self.task=conf["task"]
        except:
            pass
        if conf.has_key("document"):
            self.document=conf["document"]
        else:
            self.document=hyer.document.HTMLDocument

        if (conf.has_key("url_db")):
            self.url_db=conf["url_db"]
        else: 
            self.url_db=hyer.urldb.Urldb_mysql()

        try:
            if conf["feed"]:
                self.add_url(conf["feed"])
        except Exception,e: 
            self.logger.info("got a feed error %s" % e)
            pass
        if conf.has_key("rest_time"):
            self.rest_time=conf["rest_time"]
        else:
            self.rest_time=2

        self.browser=hyer.browser.Browser(conf["agent"])
        self.browser.setCache()
    def add_url(self,url):
        '''save an url to the meta server'''
        self.logger.info("try to add url:%s" % url)
        try:
            if self.rm.can_fetch(url):
                try:
                    self.url_db.add(url,self.task)
                except Exception,ep:
                    self.logger.info("error occured when url_db.add()")
            else:
                self.logger.info("can't fetch url: %s " % url)
        except Exception,e:
            self.logger.info("error occured when deciding if url can be crawlered or saving an url" )
            print e.message
            
    def get_all_links(self,document,url):
        ''' get all links from the document,
            all absolute urls'''
    def start(self,processes):
        for i in range(processes):
            pid=os.fork()
            if pid==0 :
                time.sleep(86400)
                return False
            self.logger.info("process %d started!" % pid)
            self.procid=pid
        self.run_loop()

    def run_loop(self):
        '''fetch tasks and finish it
        and exit when  there is no taks,'''
        go=True
        while(go):
            go=self.run_single_fetch()
            
    def run_single_fetch(self):
        ''' fetch an url,parse it,save the links,documents ....
        '''
        try:
            url=self.url_db.pop(self.task)
            if  url==None:
                self.logger.info("there is no more urls to be crawlered")
                return False
            hyer.event.fire_event("new_fetch",url)
        except StandardError,e:
            self.logger.error("error occured whe pop url:%s " % e)
            return False
        self.logger.info("new url:%s" % url)
        try:
            uri=urlparse(url)
        except:
            self.logger.info("got invalid url:%s" % url)
            return True 
        if  not self.site_holder_monster.can_visite(uri):
            self.logger.info("visited site too frequently:%s " % url)
            time.sleep(5)
            return True
        content=None
        try:
            content=self.browser.getHTML(url)
        except hyer.error.HTTPError,e:
            self.logger.error("error occured when fetching an url %s" % e)
            hyer.event.fire_event("url_fetch_error",url)
            self.url_db.mark_error(url,self.task)
            return True 
        except Exception,er:
            return True
        self.site_holder_monster.visited(uri)
        if content==None:
            self.logger.error("error occured when fetching an url %s:response is None" % url)
            return True 
		#fix the timeout problem
        doc=self.document(content,url)
        base_dir=hyer.urlfunc.get_base_dir(doc,url)
        links=[]
        all_original_links=doc["links"]
        hyer.event.fire_event("new_original_url",all_original_links)
        all_original_links=hyer.urlfunc.remove_bad_links(all_original_links)
        for l in all_original_links: 
            u=hyer.urlfunc.get_full_url(l,base_dir)
            u=hyer.urlfunc.fix_url(u)
            hyer.event.fire_event("new_fixed_url",l)
            if self.validate_url(u):
                hyer.event.fire_event("add_url",u)
                self.add_url(u)
        self.url_db.mark_visited(url,self.task)
        hyer.event.fire_event("before_save_document",doc)
        #self.save_document(doc,url,self.conf["db_path"]+"docs/")
        hyer.event.fire_event("new_document",doc)
        if self.timer > 1024:
            #self.url_db.save_to(self.conf["db_path"]+"_urls.db")
            self.timer=1
            time.sleep(1)
        else:
            self.timer =self.timer+1
        return True

    def save_document(self,document,url,path_prefix):
        ''' save the document to hard disk
            file was '''
        md5_hash=hashlib.md5(url).hexdigest()
        dir_hash=path_prefix+md5_hash[0:2]+"/"+md5_hash[2:4]
        file_name=dir_hash+"/"+md5_hash+".doc"
        if not os.path.isdir(dir_hash):
            os.system("mkdir -p "+dir_hash)
        try:
            f=open(file_name,"w")
            f.write(pickle.dumps(document))
            f.close()
        except:
            self.logger.error("can't write  documents to files")
            pass
    def teardown(self):
        '''do something ,and exit'''
        #self.url_db.save_to(self.conf["db_path"]+"_urls.db")
    def validate_url(self,u):
        '''check if the url need to be visited,
            generelly removing pictures,css and javascript files
            and if the param conf (specified when you initing the object) set leave_domain false,fire this validation
        '''
        if not self.conf["leave_domain"]:
            same_domain=False
            for sdomain_reg in self.conf["same_domain_regexps"]:
                if sdomain_reg.match(u):
                    same_domain=True
            if same_domain==False:
                return False
        if re.match(r'\.jpg$',u,re.I):
            return False 
        if re.match(r'\.gif$',u,re.I):
            return False 
        if re.match(r'\.png$',u,re.I):
            return False 
        if re.match(r'\.css$',u,re.I):
            return False 
        if re.match(r'\.js$',u,re.I):
            return False 
        return True
    def print_urls(self):
        ''' just for debug'''
        #self.url_db.debug()
