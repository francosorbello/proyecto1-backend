from .models import DonatedElement
from rest_framework import serializers
from TagAPP.models import Tag

class DonatedElementSerializer(serializers.Serializer):
    '''Permite pasar de json a model y viceversa'''
    count = serializers.IntegerField()
    tag = Tag
    description = serializers.CharField()

    def create(self, validated_data):
        return DonatedElement(**validated_data)

    def update(self, instance, validated_data):
        instance.count = validated_data.get('count',instance.rol)
        instance.tag = validated_data.get('tag',instance.name)
        instance.description = validated_data.get('description',instance.mail)
        instance.save()
        return instance