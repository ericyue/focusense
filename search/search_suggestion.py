#coding=utf-8
import HTMLParser

def search_suggestion(product_collection):
    html_parser = HTMLParser.HTMLParser()
    instant_search=product_collection.find({}, {"Property":1}).limit(500)
    
    instant_list=[]
    pname=u"品牌"
    for i in instant_search:
        for p in i['Property']:
            if p.find(pname)!=-1:
                pure_name=i['Property'][p].replace('\\','/')
                pure_name = html_parser.unescape(pure_name).strip()
                temp=pure_name.split('/')
                if len(temp)>1:
                    instant_list.append(temp[0].strip()+' '+temp[1].strip())
                else:
                    instant_list.append(pure_name)
    instant_list=set(instant_list)
    
    return instant_list