from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.renderers import JSONRenderer

from DonatedElementAPP.models import DonatedElement
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
            serializedDonations = DonationSerializer(donations,many=True)
            return Response(serializedDonations.data)
        else:
            donation = Donation.objects.get(id=pk)
            serialDonation = DonationSerializer(donation)
            return Response(serialDonation.data)
    
    def post(self,request):
        """Recibe datos dentro del request para guardar una nueva 'Donation' en la base de datos"""
        serializer = self.serializer_class(data=request.data)
        if(serializer.is_valid()):
            newDonation = serializer.create(serializer.validated_data)
            newDonation.save()
            donatedElemIds = []
            donatedElems = DonatedElement.objects.filter(donation=newDonation.id)
            for elem in donatedElems:
                donatedElemIds.append(elem.id)
            print(donatedElemIds)
            msg = "Donation created successfully"
            return Response({'message':msg,'id':newDonation.id,'donatedElemIds':donatedElemIds})
        else:
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request,pk=None):
        '''Actualiza un objeto con id pk'''
        donation = Donation.objects.get(id=pk)
        serializedDonation = DonationSerializer(donation,data=request.data)
        if(serializedDonation.is_valid()):
            serializedDonation.save()
            console.log(serializedDonation)
#            donatedElems = DonatedElement.objects.filter(donation=serializedDonation.id)
#            for elem in donatedElems:
#                donatedElemIds.append(elem.id)
            return Response({"message":"Donation updated successfully"})
        else:
            return Response(serializedDonation.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self,request,pk=None):
        '''Actualiza valores de un objeto en vez de por completo'''
        donation = Donation.objects.get(id=pk)
        serializedDonation = DonationSerializer(donation,data=request.data,partial=True)
        if(serializedDonation.is_valid()):
            newDonation = serializedDonation.save()
            print(newDonation.id)
            donatedElems = DonatedElement.objects.filter(donation=newDonation.id)
            donatedElemIds = []
            for elem in donatedElems:
                donatedElemIds.append(elem.id)

            msg = "Donation updated successfully"
            return Response({"message":msg,"id":newDonation.id,"donatedElemIds":donatedElemIds})
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