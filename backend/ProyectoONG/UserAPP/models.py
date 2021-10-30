from django.db import models

# Create your models here.
class User(models.Model):
    class UserRol(models.IntegerChoices):
        '''Enum con los roles posibles de un usuario'''
        ADMINISTRADOR = 1
        VOLUNTARIO = 2

    rol = models.IntegerField(choices=UserRol.choices) #TODO: cambiar a un enum, similar al del model de Donation
    name = models.CharField(max_length=25)
    mail = models.EmailField(max_length=50)
    password = models.CharField(max_length=15)
