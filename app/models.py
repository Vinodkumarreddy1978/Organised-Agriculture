from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Production(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    acres=models.FloatField()
    facility=models.CharField(max_length=50)
    investment=models.FloatField()
    production=models.FloatField(blank=True,null=True)
    created=models.DateField(auto_now_add=True,blank=True,null=True)
class Product(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=10)
    address=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    price=models.FloatField()