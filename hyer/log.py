#coding:utf-8
import hyer.singleton
import logging
from hyer import pcolor
import time
class Log(hyer.singleton.Singleton):
    def __init__(self,file):
        logger = logging.getLogger()
        hdlr = logging.FileHandler(file)
        #formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        formatter = logging.Formatter('%(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.NOTSET)
        self.logger=logger
    def info(self,msg):
        tmp="[%s] %s %s " % ("INFO",time.ctime(),msg)
        tmp="%s" % pcolor.pcolorstr(tmp,pcolor.PHIGHLIGHT,pcolor.PGREEN,pcolor.PBLACK)
        self.logger.info(tmp)
    def error(self,msg):
        tmp="[%s] %s %s " % ("EROR",time.ctime(),msg)
        tmp="%s" % pcolor.pcolorstr(tmp,pcolor.PHIGHLIGHT,pcolor.PRED,pcolor.PBLACK)
        self.logger.info(tmp)
    def debug(self,msg):
        tmp="[%s] %s %s " % ("DEBG",time.ctime(),msg)
        tmp="%s" % pcolor.pcolorstr(tmp,pcolor.PHIGHLIGHT,pcolor.PYELLOW,pcolor.PBLACK)
        self.logger.info(tmp)
