import redis
import re
import urllib2
from fetcher import *
from gzip_deflate_support import *
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup as BS
from threading import stack_size
import socket
def get_links(r,soup,page):
    #Parse DATA
    links=soup.findAll('a')
    newurls={}
    for textarea in soup.findAll("textarea"):
        textsoup = BS(textarea.text)  # parse the contents as html
        links.extend(textsoup.findAll("a"))
    for link in links:
        if "href" in dict(link.attrs):
            url=urljoin(page,link['href'])
            re_url=re.search(r"^(http://item\.taobao\.com/item\.htm\?id=(\d+))",url)
            if re_url:
                print '[GOOD JOB]save a item url %s ' % re_url.group().split('&')[0]
                r.zadd('product_url',re_url.group().split('&')[0],0)
            elif re.search(r'^http://.*\.taobao\.com', url):
                newurls[url]=0       
    save_url(r,newurls)
    r.zincrby('not_processed_url',page)    
            
def save_url(r,newurls):
    for(url,processed_times) in newurls.items():
        try:
            if r.zrevrank('not_processed_url',url):
                return
            r.zadd('not_processed_url',url,processed_times)
            print '[URL SAVE] url:%s... saved' %url[:60]
        except:
            print '[ERROR] error while save urls'
            pass
    return True    
