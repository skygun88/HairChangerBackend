from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uid = models.CharField(max_length=20, unique=True, primary_key=True)
    username = models.CharField(max_length=50)
    usertype = models.IntegerField(default=0) # 0: Normal user / 1: Premium user
    profile_image = models.CharField(max_length=50, null=True)