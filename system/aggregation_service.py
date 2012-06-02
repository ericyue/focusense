#coding=utf-8
#aggregation service
#MOONLIGHT LABS
#  @ERICYUE
from pymongo import Connection
from weibo import APIClient
import time
import re

#WEIBO API INFO
APP_KEY = '4054124214'
APP_SECRET = 'b1f897ad07e126d6f243f51dc9f86613'

connection =Connection('127.0.0.1',27017)
db=connection['focusense']
#WEIBO CLIENT
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET)

def run_service():
    system_weibo = db['aggregation'].find()[0]

    access_token=system_weibo['access_token']
    expires_in=system_weibo['expires_in']
    uid=system_weibo['_id']
    
    client.set_access_token(access_token, expires_in)
    
    page=1
    
    
    while(True):
        isFirst=True
        print 'Listening...'
        since=collection.find({"_id":"0"})[0]['since']
        try:
            notification = client.get.remind__unread_count(uid=uid)
        except:
            print 'Error,try again!'
            continue
        mention=int(notification['mention_status'])
        print "Mention Status:",mention
        
        if True:
            pages= 1 if mention<50 else (int(mention/50) if mention%50==0 else (int(mention/50)+1))
            count= 200
            for i in range(1,pages+1):
                print since,count,page
                try:
                    status=client.get.statuses__mentions(since_id=int(since),count=count,page=page)
                except:
                    print 'Error,try again!'
                    continue
                # print status
                if isFirst and len(status['statuses'])>0:
                    since=status['statuses'][0]['id']
                    isFirst=False
                for s in status['statuses']:
                    # print s
                    user=s['user']
                    status_id=s['id']
                    if 'retweeted_status' in s:
                        retweeted_status=s['retweeted_status']['text']
                        try:
                            pid=re.search(r'#(.*)#',retweeted_status).group().replace('#','').strip()
                        except:
                            print 'not a product status'
                            continue
                    else:
                        try:
                            pid=re.search(r'#(.*)#',s['text']).group().replace('#','').strip()
                            retweeted_status_id=None
                        except:
                            print 'not a product status'
                            continue
                    comments={
                            "pid":pid,
                            "_id":status_id,
                            "status":s
                            }
                    db['weibocomments'].insert(comments)   
                    print 'insert comments'
                time.sleep(3)
            collection.update({"_id":"0"},{"_id":"0","since":since},True)
        else:
            time.sleep(20)  
        
        
if __name__ =='__main__':
    print '=================================================================='
    print '====================Aggregation System Monitor===================='
    print '=================================================================='
    run_service()
