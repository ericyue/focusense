from django.conf.urls.defaults import *

from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'focusense.search.views.index'),
    
    (r'^item/(?P<pid>\d+)', 'focusense.search.item.item'),
    (r'^catalog$', 'focusense.system.catalog.catalog_default'),
    (r'^catalog/(?P<cid>\d+)', 'focusense.system.catalog.catalog'),
    (r'^search$', 'focusense.search.search.search'),
    
    (r'^signup$', 'focusense.system.views.signup'),
    (r'^register$', 'focusense.system.views.register'),
    (r'^login$', 'focusense.system.views.login'),
    (r'^like$', 'focusense.system.views.like'),
    (r'^share$', 'focusense.system.counts.item_share_counts'),
    (r'^likerequest', 'focusense.system.views.likerequest'),
    (r'^signup/new$', 'focusense.system.views.new'),    
    (r'^trends/$', 'focusense.system.trends.trends'),
    (r'^timeline$', 'focusense.system.timeline.timeline'),
    (r'^growing/$', 'focusense.system.growing.growing'),
        
    (r'^auth/login$', 'focusense.auth.views.login'),
    (r'^auth/callback$', 'focusense.auth.views.callback'),
    
    (r'^aggregation/prepare$', 'focusense.system.aggregation.prepare'),

    (r'^auth/logout$', 'focusense.auth.views.logout'),
    
    # (r'^.*$', 'focusense.search.views.index'),

)
if settings.DEBUG:
    urlpatterns += patterns('', (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATICFILES_DIRS})
    )
