from pymongo import Connection
from django.template import Context,loader
from django.http import HttpResponse
from taobaoke import taobaoke
from django.conf import settings

from search_suggestion import search_suggestion

from focusense.auth.weibo import *
from focusense.system.counts import *
from focusense.search.views import likerequest
from focusense.system.counts import get_hot_keys,item_visit_counts


#Sina Weibo
APP_KEY = '377160193' # app key
version=settings.VERSION
#mongodb connection
connection = Connection('localhost', 27017)
db = connection['focusense']

def item(request,pid):
    product_collection=db['product']
    db_size = product_collection.count()
    suggestion=search_suggestion(product_collection)
    hot_keys = get_hot_keys(15)
    visit_counts()
    
    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid =  request.session.get('uid',None)
    profile =db['user'].find({"_id":uid})
    if profile.count()==0:
        profile=None
    else:
        profile=profile[0]
       
    template = loader.get_template('item.html')
    item_id = pid #request.GET['id'].encode('utf-8')
    item_visit_counts(item_id)
    itemInfo = product_collection.find({"ProductID":item_id})[0]
    insert_result=None
    taokeurl=None
    try:

        taokeinfo = db['taoke'].find({"num_iid":int(item_id)})
        if taokeinfo.count()==0:
            taokeinfo=None

        if not taokeinfo:
            taoke = taobaoke('taobao.taobaoke.items.convert',itemInfo['ProductID'],'num_iid,nick,click_url,commission,commission_rate,commission_num,commission_volume,shop_click_url,seller_credit_score,volume')
            taokeinfo=db['taoke'].insert(taoke['taobaoke_items']['taobaoke_item'][0])
        try:
            taokeurl=taokeinfo[0]['click_url']
        except Exception,what:
            print what
            print 'error get clickurl'        
    except Exception, what:
        print what
        print 'error get taobaoke info'
        
    
        
    like_list=likerequest(item_id);
    recommendList=[]
    for rmd in itemInfo['RecommendList']:
        rid=rmd.split('id=')[1].strip()
        try:
            rresult=product_collection.find({"ProductID":rid})[0]
        except:
            rresult=None
        if rresult:
            recommendList.append(rresult)
    if len(recommendList)==0:
        recommendList=product_collection.find({"Catalogs.id":itemInfo['Catalogs'][1]['id']}).limit(7)
        
    weibocomments=db['weibocomments'].find({"pid":item_id})
      
        
    params_forrender={}
    if recommendList:
        params_forrender['recommendList']=recommendList
    if taokeinfo:
        params_forrender['taobaoke']=taokeurl
    if like_list:
        params_forrender['like_list']=like_list
    if profile:
        params_forrender['userProfile']=profile
    if item:
        params_forrender['item']=itemInfo
    if suggestion:
        params_forrender['instant_search']=suggestion
    if version:
        params_forrender['system_version']=version 

    if hot_keys:
        params_forrender['hot_keys']=hot_keys
    if weibocomments.count()>0:
        params_forrender['weibocomments']=weibocomments

    params = Context(params_forrender)
    return HttpResponse(template.render(params))
