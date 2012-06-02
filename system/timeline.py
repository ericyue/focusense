from django.http import HttpResponse
from pymongo import Connection
from django.template import Context,loader
from focusense.system.counts import *
from focusense.auth.weibo import *
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.conf import settings

version=settings.VERSION
connection = Connection('localhost', 27017)
db = connection['focusense']

def timeline(request): 
    visit_counts()
    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    user_uid = request.session.get('uid', None)
    
    profile =db['user'].find({"weibo_id":user_uid})
    if profile.count()==0:
        profile=None
    else:
        profile=profile[0]
    if access_token is not None:
        try:
            weibo_client = APIClient()
            weibo_client.set_access_token(access_token, expires_in)        
        except Exception,what:
            print 'error get sina auth_token'
            print what

    
    template = loader.get_template('timeline.html')
    params_forrender={}
    if version:
        params_forrender['system_version']=version
    params = Context(params_forrender)
    return HttpResponse(template.render(params))
    
