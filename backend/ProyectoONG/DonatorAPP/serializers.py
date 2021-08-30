from .models import Donator
from rest_framework import serializers

class DonatorSerializer(serializers.Serializer):
    '''Permite pasar de json a model y viceversa'''
    name = serializers.CharField(max_length=50)
    mail = serializers.EmailField()
    number = serializers.CharField(max_length=15)
    address = serializers.CharField()

    def create(self, validated_data):
        return Donator(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.mail = validated_data.get('mail',instance.mail)
        instance.number = validated_data.get('number',instance.number)
        instance.address = validated_data.get('address',instance.address)
        instance.save()
        return instance
    