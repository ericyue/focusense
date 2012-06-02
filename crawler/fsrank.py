#FSRank
import sys
import math
reload(sys)
sys.setdefaultencoding('utf-8')
def fsrank(item):
    score=0.0
    if len(item['ProductName'])<4 or len(item['ProductName'])>40:
        score-=1
    score+=0.1*len(item['PayMethodsList'])+0.2*len(item['FeaturedServicesList'])
    score+=len(item['MorePhotos'])*2.7
    score+=len(item['DetailImages'])*3
    score+=len(item['Catalogs'])*0.2
    try:
        score+=math.log10(int(item['Soldout'])+1)
    except Exception,what:
        print what
        print 'e11'
        return
    if item['Rank'].find('crown')!=-1:
        score+=int(item['Rank'].split('crown_')[1].split('.gif')[0])*50.0
    elif item['Rank'].find('cap')!=-1:
        score+=int(item['Rank'].split('cap_')[1].split('.gif')[0])*30.0
    elif item['Rank'].find('blue')!=-1:
           score+=int(item['Rank'].split('blue_')[1].split('.gif')[0])*10.0
           
    score+=len(item['RecommendList'])*0.8
    score+=len(item['CommentsTaobao'])*2
    try:
        score+=math.log10(item['ReviewsSummary']['data']['count']['good']+1)
        score+=math.log10(item['ReviewsSummary']['data']['count']['normal']+1)
        score-=math.log10(item['ReviewsSummary']['data']['count']['bad']+1)
    except Exception,what:
        print what
        print 'e12'
        return
    cor=0.0
    cor+=10*float(item['ReviewsSummary']['data']['correspondList'][0])
    cor+=6*float(item['ReviewsSummary']['data']['correspondList'][1])
    cor+=2*float(item['ReviewsSummary']['data']['correspondList'][2])
    cor-=0.1*float(item['ReviewsSummary']['data']['correspondList'][3])
    cor-=0.2*float(item['ReviewsSummary']['data']['correspondList'][4])
    cor=math.log10(cor*10+1)
    score=cor+score*(float(item['ReviewsSummary']['data']['correspond'])/5.0)
    score="%.3f" %score
    if item['isShow']:
        score+=30
        
    return score
    
