from django.db import models

# Create your models here.
class LoginInfo(models.Model):
    uid = models.CharField(max_length=20, unique=True, primary_key=True)
    password = models.CharField(max_length=30)
