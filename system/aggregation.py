#coding=utf-8
from focusense.auth.weibo import APIClient
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from pymongo import Connection
import time
from django.conf import settings

connection = Connection('localhost', 27017)
db = connection['focusense']
collection = db['aggregation']
#WEIBO API INFO
APP_KEY = '4054124214' # app key
APP_SECRET = 'b1f897ad07e126d6f243f51dc9f86613' # app secret
# CALLBACK_URL = 'http://focusense.in/auth/callback'
CALLBACK_URL = 'http://127.0.0.1:8000/auth/callback'

#API CLIENT
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)


def prepare(request):
    access_token = request.GET.get('access_token',None)
    expires_in = request.GET.get('expires_in',None)
    uid = request.GET.get('uid',None)
    
    client.set_access_token(access_token, expires_in)
    #update  token and uid
    collection.update({"_id":uid},{"_id":uid,"access_token":access_token,"expires_in":expires_in},True)
    return HttpResponse("Aggregation Service Auth Successfully !")
    
  