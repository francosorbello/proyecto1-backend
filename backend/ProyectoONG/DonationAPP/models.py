from django.db import models
from UserAPP.models import User
from CampaignAPP.models import Campaign
from DonatorAPP.models import Donator

class Donation(models.Model):
    """
    Modelo del objeto Donación

    Attributes
    -----------

    campaignId
        id de la Campaña que forma parte.
    storageAddress
        Dirección donde la Donación está almacenada
    status
        Status de la Donación, definidos por `DonationStatus`
    """
    class DonationStatus(models.IntegerChoices):
        '''
        Enum con los estados posibles de una donacion
        '''
        PENDIENTE = 1
        ASIGNADA = 2
        RECIBIDA = 3
        ENTREGADA = 4
        VENCIDA = 5

    # userId = models.ForeignKey(User,on_delete=models.CASCADE)
    campaignId = models.ForeignKey(Campaign,on_delete=models.CASCADE)
    # donatorId = models.ForeignKey(Donator,on_delete=models.CASCADE)
    storageAddress = models.CharField(max_length=200)
    status = models.IntegerField(choices=DonationStatus.choices)
