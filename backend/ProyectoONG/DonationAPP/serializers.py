from django.db.models import fields
from rest_framework import serializers

from DonatedElementAPP.serializers import DonatedElementSerializer
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    donatedElements = DonatedElementSerializer(many=True,read_only=True)    
    class Meta:
        model = Donation
        fields = ['id','campaignId','storageAddress','status','donatedElements']