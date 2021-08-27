from django.db import models
from django.db.models.fields import CharField

# Create your models here.

class Campaign(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    initialDate = models.DateField()
    endDate = models.DateField()