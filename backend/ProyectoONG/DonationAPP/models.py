from django.db import models
from UserAPP.models import User
from CampaignAPP.models import Campaign
from DonatorAPP.models import Donator

class Donation(models.Model):
    class DonationStatus(models.IntegerChoices):
        '''Enum con los estados posibles de una donacion'''
        PENDING = 1
        RECEIVED = 2
        ASSIGNED = 3
        DELIVERED = 4
        EXPIRED = 5

    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    campaignId = models.ForeignKey(Campaign,on_delete=models.CASCADE)
    donatorId = models.ForeignKey(Donator,on_delete=models.CASCADE)
    storageAddress = models.CharField(max_length=200)
    status = models.IntegerField(choices=DonationStatus.choices)
