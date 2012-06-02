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

def catalog_default(request): 
    return catalog(request,"16")
    
def catalog(request,cid): 
    visit_counts()
    access_token = request.session.get('access_token', None)
    expires_in = request.session.get('expires_in', None)
    user_uid = request.session.get('uid', None)
    if cid==None or cid==0:
        cid="16"
        # cid={ "$exists": "true" }
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

    items=db['product'].find({"Catalogs.id":cid}).sort(u"fsrank_score",-1)
    current_url=request.path
    if items and items.count() >=1:
        after_range_num = 3
        befor_range_num = 4
        try:
            page = int(request.GET.get("page",1))
            print page
            if page < 1:
                page = 1
        except ValueError:
                page = 1
        paginator = Paginator(items,20)
        try:
            result = paginator.page(page)
        except(EmptyPage,InvalidPage,PageNotAnInteger):
            result = paginator.page(paginator.num_pages)
            if page >= after_range_num:
                page_range = paginator.page_range[page-after_range_num:page+befor_range_num]    
        else:
            page_range = paginator.page_range[0:int(page)+befor_range_num]    
    else:
        result=None
        page_range=None
    
    
    template = loader.get_template('catalog.html')
    params_forrender={}
    if current_url:
        params_forrender['current_url']=current_url
    if version:
        params_forrender['system_version']=version
    if page_range:
        params_forrender['page_range']=page_range
    if result:
        params_forrender['result']=result 
    params = Context(params_forrender)
    return HttpResponse(template.render(params))
    
