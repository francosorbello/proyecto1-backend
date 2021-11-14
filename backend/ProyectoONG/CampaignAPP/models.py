from django.db import models
from django.db.models.fields import CharField

class Campaign(models.Model):
    """
    Modelo del objeto Campaña

    Attributes
    -----------
    
    name
        Nombre de la campaña.
    description
        Descripción de la campaña.
    initialDate
        Fecha en que la campaña comienza
    endDate
        Fecha en la que la campaña finaliza
    """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    initialDate = models.DateField()
    endDate = models.DateField()