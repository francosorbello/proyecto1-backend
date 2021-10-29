from django.db import models

# Create your models here.

class Donator(models.Model):
    name = models.CharField(max_length=50) #TODO: que solo acepte letras y espacios
    mail = models.EmailField(max_length=200,blank=True)
    number = models.CharField(max_length=15,blank=True) #TODO: cambiar a NumberField
    address = models.CharField(max_length=200,blank=True)