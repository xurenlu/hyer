#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

__author__ = "xurenlu"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2008 xurenlu"
__license__ = "LGPL BSD"

def sig_exit():
    print "got mesg:[2]"
    sys.exit(0)
def handler(signum, frame):
    if signum == 2:
        sig_exit()
        return None
import signal, os,time,re
signal.signal(2,handler)


#================================================
import sys, os
import hyer.document
import hyer.browser
import hyer.rules_monster
import hyer.event
import hyer.vsr
import hyer.source
import hyer.filter
import hyer.builders
import hyer.helper
import hyer.dbwriter
import hyer.production_line
import hyer.worker
import hyer.console_desk
import hyer.singleton
import hyer.log
import codecs
import sys
import json
import re
sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding("utf-8")


consoleDesk=hyer.console_desk.ConsoleDesk()
worker1=hyer.worker.Worker()
#worker1.set("name","url generator")
print worker1
log=hyer.log.Log("/var/data/amazon/hyer.log")
log.info("hi,baby")
log.error("hi,baby")
log.debug("hi,baby")
