from django.db import models

class Crawl_URL(models.Model):
    url = models.URLField('crawl url',max_length=255, unique=True)
    depth = models.SmallIntegerField('depth',default = 0)
    is_save = models.BooleanField('is_saved',default= False)
    date = models.DateTimeField('saved_time',auto_now_add=True,blank=True,null=True)
    def __unicode__(self):
        return self.url