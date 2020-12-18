from django.db import models

# Create your models here.
class RequestInfo(models.Model):
    idx = models.IntegerField(unique=True, primary_key=True)
    uid = models.CharField(max_length=20)
    rid = models.IntegerField(default=0) # request ID
    facePath = models.CharField(max_length=100)
    hairPath = models.CharField(max_length=100)
    convertedPath = models.CharField(max_length=100)
    progress = models.IntegerField(default=0) # -1: Error / 0: Not start / 1: extracting / 2: training / 3: converting / 4: done / 5: true_done