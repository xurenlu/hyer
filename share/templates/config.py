#!/usr/bin/python
#coding:utf-8
#Author:renlu.xu
#URL:http://www.162cm.com/
#date:2009.10.31

import sys

#User-agent sent to web server  by the spider 
USER_AGENT      =   "Hyer/python (a simple spider written in python"

#Max times of visits to single site  in one minute 
MAX_IN_MINUTE   =   60

#Cache single url or not
USE_CACHE       =   True

#Cache Method :memcache/diskhash/Mysqldb and so on
CACHE_METHOD    =   "DISKHASH"

#configuration used by cache methods;
CACHE_CONFIG    =   {dir:"/tmp/cache/"}

#If the site has robots.txt ,set to "True". 
ROBOTS_TXT      =   True



