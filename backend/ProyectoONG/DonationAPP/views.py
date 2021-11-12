from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.renderers import JSONRenderer
from .models import Donation

from .serializers import DonationSerializer
# Create your views here.

class DonationStatusView(APIView):
    def get(self,request):
        return Response(Donation.DonationStatus.choices)

class DonationAPPView(APIView):

    serializer_class = DonationSerializer

    def get(self,request,format = None,pk=None):
        '''retorna una lista de 'Donations' o una especifica cuando se indica su id'''
        if(pk == None):
            donations = Donation.objects.all()
            return Response(list(donations.values()))
        else:
            donation = Donation.objects.get(id=pk)
            serialDonation = DonationSerializer(donation)
            return Response(serialDonation.data)
    
    def post(self,request):
        """Recibe datos dentro del request para guardar una nueva 'Donation' en la base de datos"""
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if(serializer.is_valid()):
            newDonation = serializer.create(serializer.validated_data)
            newDonation.save()
            msg = "Donation created successfully"
            return Response({'message':msg,'id':newDonation.id})
        else:
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request,pk=None):
        '''Actualiza un objeto con id pk'''
        donation = Donation.objects.get(id=pk)
        serializedDonation = DonationSerializer(donation,data=request.data)
        if(serializedDonation.is_valid()):
            serializedDonation.save()
            return Response({"message":"Donation updated successfully"})
        else:
            return Response(serializedDonation.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self,request,pk=None):
        '''Actualiza valores de un objeto en vez de por completo'''
        donation = Donation.objects.get(id=pk)
        serializedDonation = DonationSerializer(donation,data=request.data,partial=True)
        if(serializedDonation.is_valid()):
            serializedDonation.save()
            msg = "Donation updated successfully"
            return Response({"message":msg})
        else:
            return JsonResponse(code=400, data="wrong parameters")

    def delete(self,request,pk=None):

        donation = Donation.objects.get(id=pk)
        if(donation == None):
            #TODO: implementar error 404 cdo el objeto no existe
            return Response("")
        donation.delete()
        msg = "Donation deleted successfully"
        return Response({"message":msg})