from django.db.models import fields
from rest_framework import serializers
from DonatedElementAPP.models import DonatedElement
from TagAPP.models import Tag
from DonatedElementAPP.serializers import DonatedElementSerializer
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    """
    Serializador de un objeto Donation.

    Attributes
    -----------
    
    donatedElements
        lista de los Elementos Donados relacionados a la Donación.
    campaignId
        id de la Campaña que forma parte.
    storageAddress
        Dirección donde la Donación está almacenada.
    status
        Status de la Donación, definidos por `DonationStatus`.
    id
        id del objeto serializado.

    """
    donatedElements = DonatedElementSerializer(many=True)
    class Meta:
        model = Donation
        fields = ['id','campaignId','storageAddress','status','donatedElements']

    def create(self, validated_data):
        """
        Crea un nuevo objeto Donation, junto con sus Elementos Donados relacionados

        Parameters
        -----------
        validated_data
            Datos del nuevo objeto.
        
        Returns
        --------
            Un nuevo objeto Donation.
        """
        donatedElements_data = validated_data.pop('donatedElements')
        donation = Donation.objects.create(**validated_data)
        for donationElem in donatedElements_data:
            self.createDonatedElement(donation,donationElem)

        return donation

    def createDonatedElement(self,donation,donatedElemData):
        """
        Crea un nuevo objeto DonatedElement.

        Parameters
        -----------
        
        donation
            Donación a los que los nuevos Elementos Donados pertenecen.
        donatedElemData
            Datos del nuevo Elemento Donado.
        """
        tag_data = donatedElemData.pop('tags')
        newDonatedElement = DonatedElement.objects.create(donation=donation,**donatedElemData)
        newDonatedElement.save()
        for tag in tag_data:
            newDonatedElement.tags.add(Tag.objects.get(name=tag["name"]))

    
    def update(self, instance, validated_data):
        """
        Actualiza una Donación, junto con sus elementos donados.

        Parameters
        -----------
        
        instance
            La Donación a editar.
        validated_data
            Datos con los que se actualiza la Donación y sus Elementos Donados.

        Returns
        --------
        Objeto Donation actualizado.
        """
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
        return newInstance

