from django.db.models import fields
from DonationAPP.models import Donation
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
    tags = TagSerializer(many = True)
    # donation = serializers.PrimaryKeyRelatedField(label="donation",queryset=Donation.objects.all())
    id = serializers.IntegerField()
    class Meta:
        model = DonatedElement
        fields = ['id','count','tags','description']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        donatedElement = DonatedElement.objects.create(**validated_data)
        donatedElement.tags.set(tags_data)
        return donatedElement
    
    def validate(self, attrs):
        print("validate#######")
        print(attrs)
        return super().validate(attrs)