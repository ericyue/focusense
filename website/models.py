from django.db import models
class FocusenseWebsite(models.Model):
    created_date=models.DateTimeField('created date')
    last_modify=models.DateTimeField('last modify')
    version=models.CharField(max_length=30)
    
    
