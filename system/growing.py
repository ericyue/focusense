from django.http import HttpResponse
from pymongo import Connection
from django.template import Context,loader
from focusense.system.counts import *

connection = Connection('localhost', 27017)
db = connection['focusense']
version='Demo'

def growing(request):
    collection = db['product']
    search_count=search_counts()
    visit_count=visit_counts()
    db_size = collection.count()
    user_collection = db['user']
    user_count = user_collection.count()
    template = loader.get_template('growing.html')
    params = Context({"visit_count":visit_count,"search_count":search_count,"user_count":user_count,'system_version': version,'database_size':db_size})
    return HttpResponse(template.render(params))