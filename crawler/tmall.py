#-*- coding=utf-8 -*-
import re
from BeautifulSoup import BeautifulSoup as BS
import HTMLParser
from pymongo import Connection

def tmall(source,soup):
    html_parser = HTMLParser.HTMLParser()
    try:
        html_title = soup.html.head.title.string
    except:
        return    
    #mongodb connecton
    connection = Connection('localhost', 27017)
    db = connection['focusense']
    collection = db['product']
    try:
        title=soup('input',{'name':'title'})[0]['value'].strip()
        price=soup('del',id="J_StrPrice")[0].contents[0].strip()
        pid=soup('input',{'name':'item_id'})[0]['value'].strip()
        page='http://detail.tmall.com/item.htm?id=%s' % pid
        seller_nickname=soup('input',{'name':'seller_nickname'})[0]['value'].strip()
        allow_quantity=soup('input',{'name':'allow_quantity'})[0]['value'].strip()
        photo_url=soup('img',{'id':'J_ImgBooth'})[0]['src'].strip()
        region=soup('input',{'name':'region'})[0]['value'].strip()
        print 'Product: %s |  ID: %s ' %(title,pid)
    except:
        print 'error get the product content'
        return
    #attributions list 
    itemlist=[]
    try:
        attributionlist = soup('ul',{'class':'attributes-list'})[0]
        for attribution in attributionlist.contents:
            try:
                attris = attribution.contents[0]
                attris = html_parser.unescape(attris)
                attris = attris.split(':')
                print '%s:%s' %(attris[0],attris[1])
            except:
                continue
            itemProperty = {"name":attris[0].strip(),"value":attris[1].strip()}    
            itemlist.append(itemProperty)
    except:
        print 'error get property'
        pass
    # save the product        
    try:
        productItem={ 
            "ProductName":title,
            "ProductPrice":price,
            "ProductID":pid,
            "SellerName":seller_nickname,
            "PhotoURL":photo_url,
            "ProductURL":page,
            "Region":region,
            "Property": itemlist
        }
        collection.insert(productItem)    
        print '$$$$$ added product [tmall] $$$$$'
    except:
        pass
        

