#!/usr/bin/env python
#-*- coding = utf-8 -*-
from gzip_deflate_support import *
from fetcher import *
import redis
import time
from taobao import *
from pymongo import Connection
from BeautifulSoup import BeautifulSoup as BS
import sys
r=redis.Redis(host='127.0.0.1')
def spider(numbers):
    try:
        urls=r.zrevrangebyscore('product_url',0,0,0,numbers) # (max,min) 0 refers not processed
        if len(urls)==0:
            print 'Waiting for linksengine...'
            time.sleep(5)
            return 
    except Exception, what:
        print what
        print '[ERROR] Cannot connect to the Redis server!'
        return        
    #mongodb connecton
    try:
        connection = Connection('localhost', 27017)
        db = connection['focusense']
        collection = db['product']
    except Exception, what:
        print what
        print '[ERROR] Cannot connect to the MongoDB server!'
        return
    fetcher = Fetcher(threads=numbers)
    for url in urls:
        fetcher.push(url)
    while fetcher.taskleft():
        output = fetcher.pop()
        print '[Fetcher]  %s ' % output[0]              
        content = unicode(output[1],'gb2312','ignore').encode('utf-8','ignore')
        if content=='' or content == None:
            continue
        soup=BS(content)

        if output[0].find('taobao.com')!=-1:
            taobao(output[0],soup,collection)
        elif output[0].find('tmall.com')!=-1:
            pass
        r.zincrby('product_url',output[0]) 
            
if __name__ =='__main__':
    if len(sys.argv) < 2:  
        print u'usage: command thread_numbers'
    else:
        a=int(sys.argv[1])
        while(True):
            spider(a)