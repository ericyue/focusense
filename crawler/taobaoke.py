#!/usr/bin/env python 
#codeing=utf-8
import datetime
try :
    import json
except ImportError :
    import simplejson as json
import urllib, hashlib
import base64

ENVIRONMENT = 'product' # or product
if ENVIRONMENT == 'devel' :
    AppKey     = '12552454'
    AppSecret  = 'sandbox94583e8d9c6d31fcb7afa8fa5'
    Gateway    = 'http://gw.api.tbsandbox.com/router/rest'
elif ENVIRONMENT == 'product' :
    AppKey     = '12552454'
    AppSecret  = '05a386594583e8d9c6d31fcb7afa8fa5'
    Gateway    = 'http://gw.api.taobao.com/router/rest'
else :
    import sys
    print >>sys.stderr, "ENVIRONMENT is neither devel nor product"
    sys.exit(1)
Format     = 'json'
SignMethod = 'md5'
APIVersion = '2.0'
SDKVersion = 'tao_api_python_1.0'

class Client :
    def __init__(self, **kwargs) :
        self.sys_params = {
            'app_key' : AppKey,
                    'v'       : APIVersion,
                    'format'  : Format,
                    'sign_method' : SignMethod,
                    'partner_id'  : SDKVersion
        }
        self.app_secret = AppSecret
        self.gateway = Gateway
        if kwargs :
            self.sys_params.update(kwargs)
    def sign(self, params) :
        items = params.items()
        items.sort()
        s = self.app_secret
        for i in items :
            s += '%s%s' % i
        s += self.app_secret
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest().upper()
    def execute(self, request, session = None) :
        d = self.sys_params.copy()
        api_params = request.get_api_params()
        d['method'] = request.get_method_name()
        d['timestamp'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if session is not None :
            d['session'] = session
        api_params.update(d)
        d['sign'] = self.sign(api_params)
        param_string = urllib.urlencode(d)
        url = '%s?%s' % (self.gateway, param_string)
        data_string = urllib.urlencode(api_params)
        try :
            http = urllib.urlopen(url, data_string)
            resp = json.load(http)
            http.close()
            values = resp.values()
            return values[0] if values else None
        except :
            return None
class TopRequest :
    def __init__(self, method_name) :
        self.method_name = method_name
        self.api_params = {}
    def get_api_params(self) : return self.api_params
    def get_method_name(self) : return self.method_name
    def __setitem__(self, param_name, param_value) : self.api_params[param_name] = param_value
def decode_top_parameters(top_parameters) :
    params = {}
    param_string = base64.b64decode(top_parameters)
    for p in param_string.split('&') :
        key, value = p.split('=')
        params[key] = value
    return params
def taobaoke(method,num_iids,fields):
    req = TopRequest(method)
    req['nick'] = 'hi_ericyue'
    req['fields'] = fields
    req['num_iids']=num_iids
    client = Client()
    j = client.execute(req)
    return j
def taobaoAPI_ItemCats(method,cid,fields):
    req = TopRequest(method)
    req['fields'] = fields
    req['cids']=cid
    client = Client()
    j = client.execute(req)
    return j
