from django.db import models

# Create your models here.

class contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    subject=models.CharField(max_length=50)
    message=models.CharField(max_length=100)
class feedback(models.Model):
    name=models.CharField(max_length=30)
    mobile=models.IntegerField()
    email=models.EmailField()
    feedback=models.CharField(max_length=50)
    