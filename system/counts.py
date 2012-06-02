import redis
from pymongo import Connection
from django.http import HttpResponse
from django.utils import simplejson


r=redis.Redis(host='127.0.0.1')

def search_counts():    
    get_visit_count=r.get('visit:search:count')
    return get_visit_count
def visit_counts():
    get_visit_count=r.incr('visit:pages:count')
    return get_visit_count
    
def item_visit_counts(pid):
    #counts for every item
    get_visit_count=r.zincrby('item_visit_count',pid)
    return get_visit_count
    
def get_most_visit_items():
    #most visit items
    get_visit_count=r.zrevrangebyscore('item_visit_count','+inf','-inf',0,30)
    return get_visit_count
        
def get_hot_keys(size):
    hkeys=r.zrevrangebyscore('search_keywords','+inf','-inf',0,size)
    return hkeys
    
def item_like_counts(pid):
    #counts for every item
    get_visit_count=r.zincrby('item_like_count',pid)
    return get_visit_count
def get_most_like_items():
    get_visit_count=r.zrevrangebyscore('item_like_count','+inf','-inf',0,30)
    return get_visit_count
    
def item_share_counts(request):
    pid= request.GET['pid'].encode('utf-8')
    #counts for every item
    get_visit_count=r.zincrby('item_share_count',pid)
    return HttpResponse(simplejson.dumps({'msg':'ok'}))
def get_most_share_items():
    get_share_count=r.zrevrangebyscore('item_share_count','+inf','-inf',0,30)
    return get_share_count
