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
            self.createDonatedElement(donation,donationElem)

        return donation

    def createDonatedElement(self,donation,donatedElemData):
        tag_data = donatedElemData.pop('tags')
        newDonatedElement = DonatedElement.objects.create(donation=donation,**donatedElemData)
        newDonatedElement.save()
        for tag in tag_data:
            newDonatedElement.tags.add(Tag.objects.get(name=tag["name"]))

    
    def update(self, instance, validated_data):
        #extraigo elementos donados de la data recibida
        donatedElements_data = validated_data.pop('donatedElements')
        #actualizo la donacion
        newInstance = super().update(instance, validated_data)
        
        #elimino todos los elementos donados para reemplazarlos por los nuevos
        #TODO: buscar mejor manera
        initalDonatedElements = DonatedElement.objects.filter(donation=newInstance.id)
        for elem in initalDonatedElements:
            elem.delete()

        for donatedElem in donatedElements_data:
            self.createDonatedElement(newInstance,donatedElem)
            # #extraigo los tags de la data recibida
            # tags = donatedElem.pop("tags")
            # #actualizo los elementos donados
            # donElemInstance = DonatedElement.objects.get(id=donatedElem["id"])

            # #estado inicial de los tags para ver si es necesario borrar alguna
            # donElemInstance.description = donatedElem["description"]
            # donElemInstance.count = donatedElem["count"]
            # donElemInstance.tags.clear()
            
            # donElemInstance.save()
        return newInstance

