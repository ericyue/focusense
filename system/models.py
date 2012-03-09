from django.db import models

class Info(models.Model):
	version = models.CharField(max_length=10)
	created_date = models.DateTimeField('created date')
	last_modified = models.DateTimeField('last modified')
	database_size = models.FloatField('database size')
