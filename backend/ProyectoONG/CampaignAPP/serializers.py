from datetime import date
from .models import Campaign
from rest_framework import serializers

class CampaignSerializer(serializers.Serializer):
    '''
    Serializador de un objeto campaña.

    Attributes
    -----------
    
    name
        Nombre de la campaña.
    description
        Descripción de la campaña.
    initialDate
        Fecha en que la campaña comienza
    endDate
        Fecha en la que la campaña finaliza
    id
        id del objeto campaña que fue serializado    
    '''
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(allow_blank=True)
    initialDate = serializers.DateField()
    endDate = serializers.DateField()
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        """
        Crea un nuevo objeto campaña.

        Parameters
        -----------

        validated_data
            Datos de la campaña nueva.
        """
        return Campaign(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza un objeto campaña.

        Parameters
        ---------- 

        instance
            La campaña a editar.
        validated_data
            Datos con los que se actualiza la campaña.
        """
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.initialDate = validated_data.get('initialDate',instance.initialDate)
        instance.endDate = validated_data.get('endDate',instance.endDate)
        instance.save()
        return instance
    
    def validate(self, attrs):
        """
        Valida los datos recibidos en el request.
        
        Checkea que la fecha de inicio se menor que la de fin.
        """
        if(attrs["initialDate"] > attrs["endDate"]):
            raise serializers.ValidationError("La fecha de inicio es mas grande que la de fin")
        return super().validate(attrs)