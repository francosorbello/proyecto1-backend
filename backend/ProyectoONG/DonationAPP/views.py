from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.renderers import JSONRenderer
from .models import Donation

from .serializers import DonationSerializer
# Create your views here.

class DonationAPPView(APIView):

    serializer_class = DonationSerializer

    def get(self,request,format = None,pk=None):
        '''retorna una lista de tags o uno especifico cuando se indica su id'''
        if(pk == None):
            donations = Donation.objects.all()
            return Response(list(donations.values()))
        else:
            donation = Donation.objects.get(id=pk)
            serialDonation = DonationSerializer(donation)
            return Response(serialDonation.data)
    
    def post(self,request):
        """Recibe datos dentro del request para guardar un nuevo Donation en la base de datos"""
        serializer = self.serializer_class(data=request.data)
        
        if(serializer.is_valid()):
            newDonation = serializer.create(serializer.validated_data)
            newDonation.save()
            msg = "Donation created succesfully"
            return Response({'message':msg})
        else:
            return Response(serializer.errors)

    def put(self,request,pk=None):
        '''Actualiza un objeto con id pk'''
        donation = Donation.objects.get(id=pk)
        serializedDonation = DonationSerializer(donation,data=request.data)
        if(serializedDonation.is_valid()):
            serializedDonation.save()
            return Response({"message":"Updated donation"})
        else:
            return Response(serializedDonation.errors)

    # def patch(self,request,pk=None):
    #     '''Actualiza valores de un objeto en vez de por completo'''
    #     user = User.objects.get(id=pk)
        
    #     msg = "PATCH en objeto con nombre "+user.nombre
    #     return Response({"message":msg})

    def delete(self,request,pk=None):

        donation = Donation.objects.get(id=pk)
        if(donation == None):
            #TODO: implementar error 404 cdo el objeto no existe
            return Response("")
        donation.delete()
        msg = "DELETEd donation."
        return Response({"message":msg})