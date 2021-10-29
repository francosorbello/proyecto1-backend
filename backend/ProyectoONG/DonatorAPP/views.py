# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.renderers import JSONRenderer
from .models import Donator

from .serializers import DonatorSerializer
# Create your views here.

class DonatorAPPView(APIView):

    serializer_class = DonatorSerializer

    def get(self,request,format = None,pk=None):
        '''retorna una lista de 'Donators' o uno especifico cuando se indica su id'''
        if(pk == None):
            donators = Donator.objects.all()
            return Response(list(donators.values()))
        else:
            donator = Donator.objects.get(id=pk)
            
            return Response(DonatorSerializer(donator).data)
            
    
    def post(self,request):
        """Recibe datos dentro del request para guardar un nuevo 'Donator' en la base de datos"""
        serializer = self.serializer_class(data=request.data)
        
        if(serializer.is_valid()):

            donatorMail = serializer.validated_data.get("mail")
            if Donator.objects.filter(name=donatorMail).exists():
                #TODO: añadir error correcto
                return Response({'message': "El tag ya existe"})
            else:
                newDonator = serializer.create(serializer.validated_data)
                newDonator.save()
                msg = "Donator "+newDonator.name+ " created succesfully"
                return Response({'message':msg})
        else:
            return Response(serializer.errors)

    def put(self,request,pk=None):
        '''Actualiza un objeto con id pk'''
        donator = Donator.objects.get(id=pk)
        serializedDonator = DonatorSerializer(donator,data=request.data)
        if(serializedDonator.is_valid()):
            serializedDonator.save()
            return Response({"message":"PUT funca piola"})
        else:
            return Response(serializedDonator.errors)

    # def patch(self,request,pk=None):
    #     '''Actualiza valores de un objeto en vez de por completo'''
    #     user = User.objects.get(id=pk)
        
    #     msg = "PATCH en objeto con nombre "+user.nombre
    #     return Response({"message":msg})

    def delete(self,request,pk=None):

        donator = Donator.objects.get(id=pk)
        if(donator == None):
            #TODO: implementar error 404 cdo el objeto no existe
            return Response("")
        donator.delete()
        msg = "DELETE en objeto con nombre "+donator.name
        return Response({"message":msg})