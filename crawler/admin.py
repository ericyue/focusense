from focusense.crawler.models import Crawl_URL
from django.contrib import admin
class Crawl_URLAdmin(admin.ModelAdmin):
    list_display = ('url','depth','is_save','date',)
    ordering = ('-id',)
    list_filter = ('is_save','depth','date',)
    fields = ('url','depth','is_save',)
admin.site.register(Crawl_URL, Crawl_URLAdmin)
