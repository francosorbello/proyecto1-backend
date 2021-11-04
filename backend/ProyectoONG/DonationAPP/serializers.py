from django.db.models import fields
from rest_framework import serializers
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Donation
        fields = ['id','campaignId','storageAddress','status']