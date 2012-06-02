from django.http import HttpResponse
from pymongo import Connection
from django.template import Context,loader
from focusense.system.counts import *


connection = Connection('localhost', 27017)
db = connection['focusense']
version='Demo'
def trends(request):
    most_visit_item=get_most_visit_items()
    most_like_item=get_most_like_items()
    most_share_item=get_most_share_items()
    MostVisitList=[]
    for mvi in most_visit_item:
        try:
            rresult=db['product'].find({"ProductID":mvi})[0]
        except:
            rresult=None
        if rresult:
            recommend={"pid":rresult['ProductID'],"cover":rresult['MorePhotos'],"title":rresult['ProductName'],"price":rresult['ProductPrice']}
            MostVisitList.append(recommend)
    if len(MostVisitList)==0:
        MostVisitList=None
        
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
        
    MostShareList=[]
    print most_share_item
    for mll in most_share_item:
        try:
            rresult=db['product'].find({"ProductID":mll})[0]
        except:
            rresult=None
        if rresult:
            recommend={"pid":rresult['ProductID'],"cover":rresult['MorePhotos'],"title":rresult['ProductName'],"price":rresult['ProductPrice']}
            MostShareList.append(recommend)
    if len(MostShareList)==0:
        MostShareList=None
    
    #TOP FSRANK ITEMS
    top_score=db['product'].find({"Catalogs.id":"16"}).sort(u"fsrank_score",-1).limit(20)

    



    hot_keys=get_hot_keys(500)
    collection = db['product']
    db_size = collection.count()
    template = loader.get_template('trends.html')

    params = Context({"top_score":top_score,"most_share_item":MostShareList,"most_like_item":MostLikeList,"most_visit_item":MostVisitList,"hotkeys":hot_keys,'system_version': version,'database_size':db_size})
    return HttpResponse(template.render(params))
    
