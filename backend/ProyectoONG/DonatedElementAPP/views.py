from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.renderers import JSONRenderer
from .models import DonatedElement

from DonatedElementAPP.serializers import DonatedElementSerializer
# Create your views here.

class DonatedElementAPPView(APIView):

    serializer_class = DonatedElementSerializer

    def get(self,request,format = None,pk=None):
        '''retorna una lista de 'DonatedElements' o uno especifico cuando se indica su id'''
        if(pk == None):
            delements = DonatedElement.objects.all()
            return Response(list(delements.values()))
        else:
            delement = DonatedElement.objects.get(id=pk)
            return Response(DonatedElementSerializer(delement).data)
    
    def post(self,request):
        """Recibe datos dentro del request para guardar un nuevo 'DonatedElement' en la base de datos"""
        serializer = self.serializer_class(data=request.data)
        
        if(serializer.is_valid()): 
            newDonatedElement = serializer.create(serializer.validated_data)
            newDonatedElement.save()
            msg = "Donated Element created succesfully"
            return Response({'message':msg})
        else:
            return Response(serializer.errors)

    def put(self,request,pk=None):
        '''Actualiza un objeto con id pk'''
        delement = DonatedElement.objects.get(id=pk)
        serializedElement = DonatedElementSerializer(delement,data=request.data)
        if(serializedElement.is_valid()):
            serializedElement.save()
            return Response({"message":"PUT funca piola"})
        else:
            return Response(serializedElement.errors)

    # def patch(self,request,pk=None):
    #     '''Actualiza valores de un objeto en vez de por completo'''
    #     user = User.objects.get(id=pk)
        
    #     msg = "PATCH en objeto con nombre "+user.nombre
    #     return Response({"message":msg})

    def delete(self,request,pk=None):

        delement = DonatedElement.objects.get(id=pk)
        if(delement == None):
            #TODO: implementar error 404 cdo el objeto no existe
            return Response("")
        delement.delete()
        msg = "DELETE en objeto con nombre "
        return Response({"message":msg})