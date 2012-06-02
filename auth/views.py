#coding=utf-8
from weibo import APIClient
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from pymongo import Connection
from django.conf import settings

connection = Connection('localhost', 27017)
db = connection['focusense']
collection = db['user']

SIGNUP_URL='/signup'

#SINA API INFO
APP_KEY = '4054124214'
APP_SECRET = 'b1f897ad07e126d6f243f51dc9f86613'

#if settings.DEBUG:
    # CALLBACK_URL = 'http://focusense.in/auth/callback'
CALLBACK_URL = 'http://127.0.0.1:8000/auth/callback' # callback url
#else:
#    CALLBACK_URL = 'http://focusense.in/auth/callback' # callback url
    
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

def login(request):
    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    user_uid = request.session.get('uid', None)
    
    
        
    back_to_url = get_referer_url(request)
    if access_token is not None:
        return HttpResponseRedirect(back_to_url)
    request.session['login_back_to_url'] = back_to_url
    url = client.get_authorize_url()
    return HttpResponseRedirect(url)
    
def logout(request):
    del request.session['access_token']
    del request.session['expires_in']
    del request.session['uid']
    back_to_url = get_referer_url(request)
    return HttpResponseRedirect(back_to_url)
    
def callback(request):
    try:
        code = request.GET.get('code',None)
        r = client.request_access_token(code)
        back_to_url = request.session.get('login_back_to_url', '/')
        access_token = r.access_token
        expires_in = str(r.expires_in)
        
        client.set_access_token(access_token, expires_in)
    except Exception,what:
        print what
        print 'Error get sina auth code'
        return HttpResponseRedirect(back_to_url)
        
    uid = str(client.get.account__get_uid()['uid'])
    # SAVE THE SESSION IN MONGODB
    try:
        db['session'].update({"_id":uid},{"_id":uid,"access_token":access_token,"expires_in":expires_in},True)
    except Exception,what:
        print what
        print 'ERROR UPDATE THE USER SESSTION' 
    ##################################################
    if uid=='2697703663':                           ##
        # start aggregation service                 ##
        print 'Starting Service...'                 ##
        aggregation_url="http://127.0.0.1:8000/aggregation/prepare?access_token="
        aggregation_url+=access_token+"&expires_in="+expires_in+"&uid="+uid
        return HttpResponseRedirect(aggregation_url)
    
    #normal user
    #save token and uid
    request.session['access_token'] = access_token
    request.session['expires_in'] = expires_in
    request.session['uid'] = uid

    back_to_url = request.session.get('login_back_to_url', '/')
    queryUser = collection.find({"_id":uid})
    if queryUser.count()!=0:
        #already signup
        return HttpResponseRedirect(back_to_url)
    else:
        #register
        return HttpResponseRedirect(SIGNUP_URL+'?from=sina')
        
def get_referer_url(request):
    referer_url = request.META.get('HTTP_REFERER', '/')
    host = request.META['HTTP_HOST']
    if referer_url.startswith('http') and host not in referer_url:
        referer_url = '/'
    return referer_url
