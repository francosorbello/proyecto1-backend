from .models import User
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    '''Permite pasar de json a model y viceversa'''
    rol = serializers.DecimalField(decimal_places=5, max_digits = 5)
    name = serializers.CharField(max_length=25)
    mail = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=15)

    def create(self, validated_data):
        return User(**validated_data)

    def update(self, instance, validated_data):
        instance.rol = validated_data.get('rol',instance.rol)
        instance.name = validated_data.get('name',instance.name)
        instance.mail = validated_data.get('mail',instance.mail)
        instance.password = validated_data.get('password',instance.password)
        instance.save()
        return instance