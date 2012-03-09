from django.http import HttpResponse
from focusense.system.models import Info
def version(request):
    info=Info.objects.all()
    version=info[0].version;
    return HttpResponse(version)
