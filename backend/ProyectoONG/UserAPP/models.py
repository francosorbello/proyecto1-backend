from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class User(models.Model):
    rol = models.IntegerField() #TODO: cambiar a un enum, similar al del model de Donation
    name = models.CharField(max_length=25)
    mail = models.EmailField(max_length=50)
    password = models.CharField(max_length=15)
