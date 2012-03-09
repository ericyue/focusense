from django.http import HttpResponse
from django.template import Context,loader
from focusense.system.models import Info
    
def index (request):
    template = loader.get_template('search/index.html')
    info = Info.objects.all()
    #version = info[0].version
    #params = Context({'system_version': version,},{'templatePath':getTemplatePath()})
    params = Context({'TEMPLATE_PATH':getTemplatePath()})
    return HttpResponse(template.render(params))
def getTemplatePath():
    return "/Users/ericyue/python/focusense/templates/"