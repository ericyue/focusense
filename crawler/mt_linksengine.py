#!/usr/bin/env python
#-*- coding = utf-8 -*-

#Links Cache Engine 
#python mt_linksengine.py
#MAIN
#

from gzip_deflate_support import *
from fetcher import *
from parse_html import *
import sys
import redis
from BeautifulSoup import BeautifulSoup as BS
from mt_linkscache import *
def linksengine(tnum):
    try:
        r=redis.Redis(host='127.0.0.1')
        urls=r.zrevrangebyscore('not_processed_url',0,0,0,300) # (max,min) 0 refers not processed
    except Exception,what:
        print what
        print '[ERROR] error connect to redis server'
        return
        
    fetcher = Fetcher(threads=tnum)
    for url in urls:
        fetcher.push(url)
    while fetcher.taskleft():
        output = fetcher.pop()
        url=output[0] 
        print '[INFO] get links from  %s...' % url[:60]
        content = unicode(output[1],'gb2312','ignore').encode('utf-8','ignore')
        try:
            soup=BS(content)
        except Exception,what:
            print what
            print '[ERROR] Soup the Content,Return'
            continue
        if soup:
            get_links(r,soup,url)
            
if __name__ =='__main__':
    if len(sys.argv) < 2:  
        print u'Specify the thread numbers : '
    else:
        a=int(sys.argv[1])
        while(True):
            linksengine(a)