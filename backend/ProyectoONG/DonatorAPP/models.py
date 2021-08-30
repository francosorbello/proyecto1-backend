from django.db import models

# Create your models here.

class Donator(models.Model):
    name = models.CharField(max_length=50)
    mail = models.EmailField(max_length=200)
    number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)