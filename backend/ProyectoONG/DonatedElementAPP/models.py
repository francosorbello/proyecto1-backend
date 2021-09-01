from django.db import models
from TagAPP.models import Tag

# Create your models here.
class DonatedElement(models.Model):
    count = models.IntegerField()
    tag = Tag
    description = models.TextField(blank=True)
