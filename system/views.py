#coding=utf-8
#MOONLIGHT LABS
#ERICYUE

from django.http import HttpResponse
from django.http import HttpRequest
from django.template import Context,loader
from django.http import HttpResponseRedirect

from pymongo import Connection
from focusense.auth.weibo import *
from django.utils import simplejson
from focusense.system.counts import item_like_counts
import redis

#MONGODB CONNECTION
connection = Connection('localhost', 27017)
db = connection['focusense']
#REDIS CONNECTION
r=redis.Redis('127.0.0.1')
version='Demo'

access_token=None
expires_in=None
uid=None
profile=None

def login(request):
    password = request.GET['password']  
    email = request.GET['email']
    # print email,password
    queryUser = db['user'].find({"email":email,"password":password})
    if queryUser.count()!=0:
        #ALREAD SIGN UP
        return HttpResponse(simplejson.dumps({'msg':'ok'}))  
    else:
        #NEW HERE
        return HttpResponse(simplejson.dumps({'msg':'error'}))  
        
def signup(request):
    global access_token
    global expires_in
    global uid
    global profile
    
    template = loader.get_template('signup.html')
    type = request.GET['from'].encode('utf-8') 
    back_to_url = request.session.get('login_back_to_url', '/')
    #GET FROM AUTH
    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    uid =  request.session.get('uid',None)
    
    if type=='sina':
        #FROM SINA WEIBO
        if access_token is not None:
            try:
                weibo_client = APIClient()
                weibo_client.set_access_token(access_token, expires_in)
                profile = weibo_client.get.users__show(uid=uid)
                profile['from']=u'新浪微博'
                
            except Exception,what:
                print what
                print 'error get profile'
                return HttpResponseRedirect(back_to_url)
        print profile
    elif type=='qq':
        #qq
        pass
    elif type=='renren':
        #renren
        pass
    params = Context({'userProfile':profile,'system_version': version})
    return HttpResponse(template.render(params))
    
def like(request):
    global uid
    pid= request.GET['pid']
    if uid==None:
        uid= request.session.get('uid',None)
    item_like_counts(pid)
    req=db['like'].update({"pid":pid},{"$push":{"uid":uid}},True)
    return HttpResponse(simplejson.dumps({'msg':'ok'}))
       
def register(request):
    global access_token
    global expires_in
    global uid
    global profile
    del profile['status']

    if request.method == 'GET':  
            password = request.GET['password']  
            email = request.GET['email']  
            newuser={
                "_id":str(profile['id']),
                "email":email,
                "password":password,
                "detail":profile                
            }
            user = db['user'].insert(newuser)
            # print user
            if user is not None:  
                return HttpResponse(simplejson.dumps({'msg':'ok'}))  
            else:  
                return HttpResponse(simplejson.dumps({'msg':'error'}))    


