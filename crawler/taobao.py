#-*-coding:utf-8-*-
#CRAWLER FOR TAOBAO.COM
#FOCUSENSE.IN
#ERICYUE.INFO
import re
import HTMLParser
from BeautifulSoup import BeautifulSoup as BS
from taobaoke import taobaoAPI_ItemCats
import urllib2
from puretitle import puretitle
import json
import socket
from fsrank import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
socket.setdefaulttimeout(100)

#FILTERS OF ITEMS
REVIEWS_SUMMARY_MARKS=55
PRICE_TOP=400000.0
PRICE_BOTTOM=2.0
SOLD_OUT_NUMBERS=3
COMMENTS_NUMBERS=2

def taobao(source,soup,collection):
    #isShow
    #ONLY IF THE PRODUCT'S COVER PICTURES IS PURE ENOUGH! 
    #SET MANUALLY 
    try:    
           pid=source.split('id=')[1].strip()
           # pid=soup('input',{'name':'item_id'})[0]['value'].strip()
    except Exception, what:
        print what
        print 'error get pid'
        return
    print '[%s] get pid'  %pid
    try:
        cids=[]
        cid=soup('div',{"id":'J_itemViewed'})[0]['catid']
    except Exception, what:
        print what
        print 'error get cid number'
        return

    
    page=source
    try:
        shop_rank=soup('img',{"class":"rank"})[0]['src'].strip()
    except Exception, what:
        print what
        print '[ERROR]error get the shop rank'
        return
    if not (shop_rank.find('cap')!=-1 or shop_rank.find('crown')!=-1 or shop_rank.find('blue')!=-1):
        print '[ERROR] shop rank too low ,return !'
        return
    print '[%s] get shoprank,enough!' %pid 
        
    html_parser = HTMLParser.HTMLParser()
    try:
        html_title = soup.html.head.title.string
    except Exception, what:
        print what
        print '[ERROR] error get the page title'
        return
    print '[%s] get title'  %pid  

    title=html_title[:len(html_title)-4].strip()
    title = html_parser.unescape(title).strip()
    try:
        title = puretitle(title) #Pure Title
    except Exception, what:
        print what
        print '[ERROR] cannot pure title'
        print title
        pass
    try:
        price=soup('strong',id="J_StrPrice")[0].contents[0].strip()
        tmp_price=price.split('-')[0]
        if float(tmp_price)>PRICE_TOP or float(tmp_price)<PRICE_BOTTOM:
            print '[BAD　PRODUCT] PRICE IS ABNORMAL , DROP!'
            return 
    except Exception, what:
        print what
        print 'error get price'
    print '[%s] get price'  %pid  
    

    
    try:
        seller_nickname=soup('a',{'class':'hCard fn'})[0].contents[0]
    except Exception, what:
        print what
        print 'error get seller name'
    print '[%s] get seller_nickname'   %pid 

    try:
        shop_url=soup('a',{'class':'hCard fn'})[0]['href'].strip()
        shop_url=shop_url.split("?spm")[0]
    except Exception, what:
        print what
        print 'error get shop url'
    print '[%s] get shop_url'   %pid 

    try:
        shopinfo=soup('meta',{"name":"microscope-data"})[0]['content'].split(';') 
        seller_id=shopinfo[4].strip().split('=')[1]
        shop_id=shopinfo[3].strip().split('=')[1]
        
    except Exception, what:
        print what
        print 'error get shop info' 
        return
    print '[%s] get shopinfo' %pid   
    
    try:
        reviews_summary_query='http://rate.taobao.com/detailCommon.htm?userNumId='+seller_id+'&auctionNumId='+pid+'&siteID=&callback=jsonp_reviews_summary'
        reviews_summary=urllib2.urlopen(reviews_summary_query).read() 
        json_content="".join(re.search('\{([\s\S]*)\}',reviews_summary).group().split())
        # print json_content
        try:
            reviews_summary=json.loads(json_content)
        except Exception:
            reviews_summary=''
        try:
            if float(reviews_summary['data']['correspondList'][0])<REVIEWS_SUMMARY_MARKS:
                print '[BAD　PRODUCT] The Product is BAD in reviews.Drop it!'
                return
        except Exception,what:
		    pass
    except Exception, what:
        print what
        print 'error get reviews_summary'
        return
    print '[%s] get reviews_summary' %pid
    
        
    product_images=[]
    #get the product images list
    try:
        images=soup('div',{"class":"tb-pic tb-s40"})
        for image in images:
            image_url=image.contents[1].contents[0]['src']
            image_url=image_url.split('_40')[0]
            product_images.append(image_url.strip())
        if len(product_images)==0:
            product_images=None
            return
    except Exception, what:
        print what
        print 'error get the product description photos'
        return
    print '[%s] get product_images' %pid   

    detail_images=[]
    
    try:
        req=soup('textarea',{"class":"bigrender-data","data-priority":"0"})
        detail_url=''
        req=req[0].contents[0].split(',')
        for r in req:
            r=r.split(':"')
            r[0]=r[0].strip()
            if r[0]=='"apiItemDesc"':
                r[1]=r[1][0:(len(r[1])-1)]
                detail_url=r[1]
                break                    
                
        detail = urllib2.urlopen(detail_url).read() 
        detail = unicode(detail,'gb2312','ignore').encode('utf-8','ignore')
        # get the product images list
        soup_detail=BS(detail)
        images=soup_detail('img',{"align":"absMiddle"})
        if len(images)==0:
            images=soup_detail('img',{"align":"middle"})
        for image in images:
            try:
                image_url=image['src']
                # print image_url
            except Exception, what:
                print what
            if image_url.find('_!!')!=-1:
                  detail_images.append(image_url.strip())
                  # print image_url.strip()
            else:
                  continue
           
    except Exception, what:
        print what
        print 'error get the product detail photos'
        return
    print '[%s] get detail photos' %pid   

    #attributions list 
    itemlist=dict()
    try:
        attributionlist = soup('ul',{'class':'attributes-list'})[0]
        for attribution in attributionlist.contents:
            try:
                attris = attribution.contents[0]
            except Exception, what:
                continue
            try:
                attris = html_parser.unescape(attris).strip()
            except Exception, what:
                continue
            try:
                attris = attris.replace(u'：',':').split(':')
            except Exception, what:
                continue  
            try:
                itemlist[attris[0].strip()]=attris[1].strip()
            except Exception, what:
                continue
        if len(itemlist)==0:
            print 'empyt attri'
            return
    except Exception, what:
        print what
        print 'error get property list'
        return
    print '[%s] get attributions'  %pid  
    # print itemlist
    shop_rate=dict()
    try:
        rate_items=soup('div',{"class":"shop-rate"})[0]('li')
        for item in rate_items:
            shop_rate[item.contents[0].strip()]=item.contents[1]('em')[0].contents[0].strip()
    except:
        print 'error get shop_rate'
        

    
    try:
        sold_quest='http://detailskip.taobao.com/json/deal_quantity.htm?isStart=false&external=false&exterShop=false&sellerId='+seller_id+'&id='+pid+'&shopId=&aucType=b&isarchive=&cartBut=true&callback=TShop.mods.SKU.SetDealCounts.render'
        headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        'Referer':page
        }
        req = urllib2.Request(
            url = sold_quest,
            headers = headers
            
        )
        sold_out=urllib2.urlopen(req).read() 
        sold_out=sold_out.split('y:')[1].split(',')[0].strip()
        if int(sold_out)<SOLD_OUT_NUMBERS:
            print '[BAD PRODUCT] SOLD OUT NUMBER TOO LOW,DROP!'
            return
        # print sold_out
    except Exception, what:
        print what
        print 'error get soldout number'
        return 
    print '[%s] get sold_out'  %pid  
    
       

    try:
        comments_taobao='http://rate.taobao.com/feedRateList.htm?userNumId='+seller_id+'&auctionNumId='+pid+'&currentPageNum=1&orderType=sort_weight&showContent=1'
        comments_taobao=urllib2.urlopen(comments_taobao).read()
        comments_taobao=unicode(comments_taobao,'gb2312','ignore').encode('utf-8','ignore')
        comments_taobao=json.loads(re.search('\{(.*)\}',comments_taobao).group())['comments'] #page1
        if len(comments_taobao)<COMMENTS_NUMBERS:
            print '[BAD PRODUCT] Comments too low!'
            return
    except Exception, what:
        print what
        print 'error get comments_taobao'
        return
    print '[%s] get comments_taobao'  %pid  
        
    try:
        recommendlist=[]
        rstShopcatlist=soup('textarea',{"class":"bigrender-data","data-priority":"0"})[0].contents[0].split('rstShopcatlist:"')[1].split('",')[0]
        rstUrl='http://detailskip.taobao.com/recommended_same_type_items.htm?shopId='+shop_id+'&auctionId='+pid+'&shopcatlist='+rstShopcatlist+'&count=10'
        recommended_same_type_items=urllib2.urlopen(rstUrl).read()
        recommended_same_type_items=unicode(recommended_same_type_items,'gb2312','ignore').encode('utf-8','ignore')
        reSoup=BS(recommended_same_type_items)
        recommended_same_type_items=reSoup('a',{"class":"permalink"})
        for item in recommended_same_type_items:
            # print item['href']
            recommendlist.append(item['href'])
    except Exception, what:
        print what
        print 'error get recommended_same_type_items'
    print '[%s] get recommendlist' %pid 
    # save the product        
    pay_methods_list=[]
    featured_services_list=[]
    try:
        pay_methods=soup('div',{"class":"tb-extrainfo"})[0]('dl',{"class":"tb-paymethods J_ToggleContainer"})[0]('a',{"target":"_blank"})
        for pay in pay_methods:
            pay_methods_list.append(pay.text.strip())
        featured_services=soup('div',{"class":"tb-extrainfo"})[0]('dl',{"class":"tb-featured-services tb-featured-services-icon J_ToggleContainer"})[0]('a',{"target":"_blank"})
        for service in featured_services:
            featured_services_list.append(service['title'])
    except:
        pass
    print '[%s] get pay_methods_list and featured_services_list'  %pid  
    
    try:    
        cat_taoke_json=taobaoAPI_ItemCats('taobao.itemcats.get',cid,'parent_cid,name')
        # print cat_taoke_json
        cat_name = cat_taoke_json['item_cats']['item_cat'][0]['name']
        parent_cid=cat_taoke_json['item_cats']['item_cat'][0]['parent_cid']
        # print # cid,cat_name
        cids.append({"id":str(cid),"value":cat_name.strip()})
        while parent_cid!=0:
            cat_taoke_json=taobaoAPI_ItemCats('taobao.itemcats.get',parent_cid,'parent_cid,name')
            cat_name = cat_taoke_json['item_cats']['item_cat'][0]['name']
            # print parent_cid,cat_name
            cids.append({"id":str(parent_cid),"value":cat_name.strip()})
            parent_cid=cat_taoke_json['item_cats']['item_cat'][0]['parent_cid']     
    except Exception, what:
        print what
        print 'error get cats info'
        return
    print '[%s] get cid list'  %pid
    
    
    try:
        productItem={
            "_id":pid,
            "ProductName":title,
            "ProductPrice":price,
            "PayMethodsList":pay_methods_list,
            "FeaturedServicesList":featured_services_list,
            "ProductID":pid,
            "SellerName":seller_nickname,
            "ShopURL":shop_url,
            "SellelID":seller_id,
            "ShopID":shop_id,
            "MorePhotos":product_images,
            "DetailImages":detail_images,
            "Catalogs":cids,
            "ProductURL":page,
            "Soldout":sold_out,
            "ShopRate":shop_rate,
            "Rank":shop_rank,
            "RecommendList":recommendlist,
            "ReviewsSummary":reviews_summary,
            "CommentsTaobao":comments_taobao,
            "Property": itemlist,
            "From":'taobao'
        }
        fsrank_score=fsrank(productItem)
        productItem['fsrank_score']=str(fsrank_score)
        collection.insert(productItem)
        print '==================================================================================================='
        print '======== [Success] added product [taobao.com]'
        print '======== Product: %s |  ID: %s ' %(title,pid)
        print '==================================================================================================='
        # print detail_images
        # print productItem
        # for attri in itemlist:
        #      print attri       
    except Exception,what:
                
#print what
        #print 'error update mongodb product table'
        pass
        

