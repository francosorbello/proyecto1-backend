from django.db import models

# Create your models here.
class Tag(models.Model):
    """
    Modelo del objeto Tag
    
    ...
    Attributes
    ----------
    name : str
        Nombre del tag
    """
    name = models.CharField(max_length=25)
