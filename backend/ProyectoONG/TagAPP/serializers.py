from .models import Tag
from rest_framework import serializers

# class TagSerializer(serializers.Serializer):
#     '''Permite pasar de json a model y viceversa'''
#     name = serializers.CharField(max_length=25)

#     def create(self, validated_data):
#         return Tag(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name',instance.name)
#         instance.save()
#         return instance
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'