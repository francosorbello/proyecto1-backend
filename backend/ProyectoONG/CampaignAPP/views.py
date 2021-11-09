
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.renderers import JSONRenderer
from .models import Campaign
import datetime

from CampaignAPP.serializers import CampaignSerializer
# Create your views here.

class CampaignAPPView(APIView):

    serializer_class = CampaignSerializer

    def get(self,request,format = None,pk=None):
        '''retorna una lista de 'Campaigns' o una especifica cuando se indica su id'''
        if(pk == None):
            campaigns = Campaign.objects.all()
            onlyActive = request.query_params.get('onlyActive')
            if(onlyActive == "true"):
                activeCampaigns = filter(lambda campaign : campaign.endDate > datetime.date.today(), campaigns)
                responseList = []
                for camp in list(activeCampaigns):
                    responseList.append(CampaignSerializer(camp).data)
                return Response(responseList)
            else:
                return Response(list(campaigns.values()))
        else:
            campaign = Campaign.objects.get(id=pk)
            return Response(CampaignSerializer(campaign).data)
    
    def post(self,request):
        """Recibe datos dentro del request para guardar una nueva 'Campaign' en la base de datos"""
        serializer = self.serializer_class(data=request.data)
        
        if(serializer.is_valid()):
            newCampaign = serializer.create(serializer.validated_data)

            if(newCampaign.initialDate > newCampaign.endDate):
                return Response({'message': "La fecha de inicio es posterior a la de fin"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            newCampaign.save()

            msg = "Campaign "+newCampaign.name+ " created successfully"
            return Response({'message':msg,"id":newCampaign.id})
        else:
            return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request,pk=None):
        '''Actualiza un objeto con id pk'''
        campaign = Campaign.objects.get(id=pk)
        serializedCampaign = CampaignSerializer(campaign,data=request.data)
        if(serializedCampaign.is_valid()):
            serializedCampaign.save()
            return Response({"message":"Campaign updated successfully"})
        else:
            return Response(serializedCampaign.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self,request,pk=None):
        '''Actualiza un objeto con id pk'''
        campaign = Campaign.objects.get(id=pk)
        serializedCampaign = CampaignSerializer(campaign,data=request.data,partial=True)
        if(serializedCampaign.is_valid()):
            serializedCampaign.save()
            return Response({"message":"Campaign updated successfully"})
        else:
            return Response(serializedCampaign.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,pk=None):

        campaign = Campaign.objects.get(id=pk)
        if(campaign == None):
            #TODO: implementar error 404 cdo el objeto no existe
            return Response("")
        campaign.delete()
        msg = "Campaign "+campaign.name+ " deleted successfully"
        return Response({"message":msg})