from django.db.models import fields
from rest_framework import serializers
from DonatedElementAPP.models import DonatedElement
from TagAPP.models import Tag
from DonatedElementAPP.serializers import DonatedElementSerializer
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    donatedElements = DonatedElementSerializer(many=True)    
    class Meta:
        model = Donation
        fields = ['id','campaignId','storageAddress','status','donatedElements']

    def create(self, validated_data):
        donatedElements_data = validated_data.pop('donatedElements')
        donation = Donation.objects.create(**validated_data)
        for donationElem in donatedElements_data:
            tag_data = donationElem.pop('tags')
            newDonatedElement = DonatedElement.objects.create(donation=donation,**donationElem)
            newDonatedElement.save()
            for tag in tag_data:
                newDonatedElement.tags.add(Tag.objects.get(name=tag["name"]))

        return donation
    
    def update(self, instance, validated_data):
        donatedElements_data = validated_data.pop('donatedElements')
        newInstance = super().update(instance, validated_data)
        for donatedElem in donatedElements_data:
            print(donatedElem)
            # donElemInstance = DonatedElement.objects.get(id=donatedElem["id"])
            # print(donElemInstance)
        return newInstance