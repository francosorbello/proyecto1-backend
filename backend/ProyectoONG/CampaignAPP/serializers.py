from .models import Campaign
from rest_framework import serializers

class CampaignSerializer(serializers.Serializer):
    '''Permite pasar de json a model y viceversa'''
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(allow_blank=True)
    initialDate = serializers.DateField()
    endDate = serializers.DateField()

    def create(self, validated_data):
        return Campaign(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.initialDate = validated_data.get('initialDate',instance.initialDate)
        instance.endDate = validated_data.get('endDate',instance.endDate)
        instance.save()
        return instance
    