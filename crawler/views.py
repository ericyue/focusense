from django.http import HttpResponse
from django.template import Context,loader
from focusense.crawler.mt_spider import *
from focusense.crawler.links_cache import *

def run (request):
    crawler()
    return HttpResponse("Run")
def mt_spider (request):
    spider()
    return HttpResponse("spider")
def links_cache (request):
    get_links()
    return HttpResponse("links")