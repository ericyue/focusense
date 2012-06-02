# -*- coding: utf-8 -*-
#support chinese

import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def puretitle(title): 
    title=title.replace(u'淘金币','').replace(u'特价','').replace(u'正品','').replace(u'~','').replace(u'☆',' ').replace(u'★',' ')
    title=title.replace(u'*',' ').replace(u'_',' ').replace(u'/',' ').replace(u'!',' ').replace(u'！',' ').replace(u'“',' ').replace(u'”',' ')
    title=title.replace(u'\\',' ').replace(u'+',' ').replace(u'#',' ').replace(u'"',' ').replace(u'＃',' ')
    #get rid of the [ xxxx ]
    title=re.sub(r'\【.*】|\[.*]|\［.*］|\(.*\)|\（.*\）','',title.encode('utf-8')).replace('『',' ').replace('』',' ').replace('--','-')
    title=title.replace(u'(',' ').replace(u')',' ').replace(u'（',' ').replace(u'）',' ')
    title=title.replace(u'【',' ').replace(u'】',' ').replace(u'［',' ').replace(u'］',' ').replace(u'、',' ').replace(u',',' ').replace(u'|',' ')
    title=title.upper().strip()
    return title
