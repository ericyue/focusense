from pymongo import Connection
from pymmseg import mmseg
from django.template import Context,loader
from django.http import HttpResponse
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from search_suggestion import search_suggestion
from focusense.system.hotkeywords import get_hot_keys
from focusense.system.counts import *
from django.conf import settings
import redis
import re

#redis connection
r=redis.Redis(host='127.0.0.1')
#mongodb connection
connection = Connection('localhost', 27017)
db = connection['focusense']
version=settings.VERSION
#support chinese
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#main function begin
def guess_what_you_like():
    #random item
    collection = db['product']
    head=int(random.uniform(1,500))
    bottom=int(random.uniform(head+1,1000))
    val=int(random.uniform(head,botton))
    guess_list=collection.find().limit(bottom+2)
    
    return guess_list
def search (request):
    hot_keys = get_hot_keys(40)
    r.incr('visit:search:count')
    visit_counts()
    suggestion=search_suggestion(db['product'])
    mmseg_keys=[]
    collection = db['product']
    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid = request.session.get('uid', None)
    
    profile =db['user'].find({"_id":uid})
    if profile.count()==0:
        profile=None
    else:
        profile=profile[0]
    #chinese word segmentation engine
    mmseg.Dictionary.load_dictionaries()
    db_size = collection.count()
    template = loader.get_template('search.html')
    keywords = request.GET['keys'].encode('utf-8')
    current_url=request.path+'?keys='+keywords
    seg_keys=[]
    patterns=[]
    search_str=''
    
    mmseg_keys_temp = mmseg.Algorithm(keywords)
    for tok in mmseg_keys_temp:
        mmseg_keys.append(tok.text)
    
    if len(keywords)>30:
        algor = mmseg.Algorithm(keywords)
        for tok in algor:
            seg_keys.append(tok.text)
            patterns.append(re.compile('.*%s.*'%tok.text))
            search_str=search_str+'.*'+tok.text+'.*|'
    else:
        algor=keywords.split(' ')
        for tok in algor:
            #add to redis server statics
            seg_keys.append(tok.strip())
            patterns.append(re.compile('.*%s.*'%tok.strip()))
            search_str=search_str+'.*'+tok+'.*|'
        
    #restrict search 
    result_list=collection.find({"ProductName":{"$all":patterns}})
    if result_list.count()==0:
        
        #restrict search return none,then use the loose search method
        search_str=search_str.rstrip('|')
        pattern = re.compile(search_str)
        result_list=collection.find({"ProductName":pattern})
    if keywords.strip()=='':
        result_list=None
        
    if result_list and result_list.count() >=1:
        algor=keywords.split(' ')
        for tok in algor:
            try:
                if tok.strip()!='':
                    r.zincrby('search_keywords',tok)
            except:
                print 'error redis search static'
        after_range_num = 3
        befor_range_num = 4
        try:
            page = int(request.GET.get("page",1))
            if page < 1:
                page = 1
        except ValueError:
                page = 1
        paginator = Paginator(result_list,10)
        try:
            search_result = paginator.page(page)
        except(EmptyPage,InvalidPage,PageNotAnInteger):
            search_result = paginator.page(paginator.num_pages)
            if page >= after_range_num:
                page_range = paginator.page_range[page-after_range_num:page+befor_range_num]    
        else:
            page_range = paginator.page_range[0:int(page)+befor_range_num]    
    else:
        algor=keywords.split(' ')
        for tok in algor:
            r.zincrby('search_keywords_not_exist',tok)
        search_result=None
        page_range=None
        
        
    most_like_item=get_most_like_items()
    MostLikeList=[]
    for mll in most_like_item:
        try:
            rresult=db['product'].find({"ProductID":mll})[0]
        except:
            rresult=None
        if rresult:
            recommend={"pid":rresult['ProductID'],"cover":rresult['MorePhotos'],"title":rresult['ProductName'],"price":rresult['ProductPrice']}
            MostLikeList.append(recommend)
    if len(MostLikeList)==0:
        MostLikeList=None
        
    params = Context({"MostLikeList":MostLikeList,"mmseg_keys":mmseg_keys,"hotkeys":hot_keys,"current_url":current_url,'page_range':page_range,'userProfile':profile,'result_list':search_result,'instant_search':suggestion,'search_key_words':seg_keys,'system_version': version,'database_size':db_size})
    return HttpResponse(template.render(params))