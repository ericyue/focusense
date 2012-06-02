#coding=utf-8
from django.http import HttpResponse
import re
from focusense.system.counts import *
from focusense.auth.weibo import *
from django.template import Context,loader
from django.conf import settings

from pymongo import Connection
from pymmseg import mmseg
from search_suggestion import search_suggestion
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage

#mongodb connection
connection = Connection('localhost', 27017)
db = connection['focusense']

version=settings.VERSION
#support chinese
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

suggestion=search_suggestion(db['product'])

def index (request):
    visit_counts()
    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)  
    try:
        
        profile =db['user'].find({"_id":uid})
        if profile.count()==0:
            profile=None
        else:
            profile=profile[0]
    except:
        pass
    collection = db['product']    
    db_size = collection.count()
    template = loader.get_template('index.html')
    params= Context({'userProfile':profile,'instant_search':suggestion,'system_version':version,'database_size':db_size})
    return HttpResponse(template.render(params))

def commentFromTaobao(request):
    try:
        item_id = request.GET['cpage'].encode('utf-8')
        comments_taobao='http://rate.taobao.com/feedRateList.htm?userNumId='+seller_id+'&auctionNumId='+pid+'&currentPageNum='+cpage+'&orderType=sort_weight&showContent=1'
        comments_taobao=urllib2.urlopen(sold_quest).read()
        comments_taobao=json.loads(re.search('\{(.*)\}',c).group())['comments'] #page1
        return comments_taobao
    except:
        print 'error get comments_taobao'
        
def likerequest(pid):
    likelist=None
    try:
        collection = db['like']
        likelist=collection.find({"pid":pid})[0]
        likelist = list(set(likelist['uid']))
    except Exception, what:
        likelist=None
    if not likelist:
        return None
    imglist=[]
    for item in likelist:
        imglist.append(db['user'].find({"_id":item})[0]['detail']['profile_image_url'])
    return imglist
  
