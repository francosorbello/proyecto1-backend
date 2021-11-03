from django.db.models import fields
from TagAPP.serializers import TagSerializer
from .models import DonatedElement
from rest_framework import serializers
from TagAPP.models import Tag

# class DonatedElementSerializer(serializers.Serializer):
#     '''Permite pasar de json a model y viceversa'''
#     count = serializers.IntegerField()
#     tags = TagSerializer(many=True)
#     description = serializers.CharField(allow_blank=True)

#     def create(self, validated_data):
#         return DonatedElement(**validated_data)

#     def update(self, instance, validated_data):
#         instance.count = validated_data.get('count',instance.count)
#         instance.tag = validated_data.get('tag',instance.tag)
#         instance.description = validated_data.get('description',instance.description)
#         instance.save()
#         return instance

class DonatedElementSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(many = True)
    class Meta:
        model = DonatedElement
        fields = ['id','count','tags','description']
        depth = 1
