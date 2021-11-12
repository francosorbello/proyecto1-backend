from django.db import models
from DonationAPP.models import Donation
from TagAPP.models import Tag

# Create your models here.

class DonatedElement(models.Model):
    count = models.IntegerField()
    tags = models.ManyToManyField(Tag,related_name="tags")
    description = models.TextField(blank=True)
    donation = models.ForeignKey(Donation,on_delete=models.CASCADE,related_name='donatedElements')