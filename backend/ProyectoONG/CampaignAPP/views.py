
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.renderers import JSONRenderer
from .models import Campaign

from CampaignAPP.serializers import CampaignSerializer
# Create your views here.

class CampaignAPPView(APIView):

    serializer_class = CampaignSerializer

    def get(self,request,format = None,pk=None):
        '''retorna una lista de usuarios o uno especifico cuando se indica su id'''
        if(pk == None):
            campaigns = Campaign.objects.all()
            return Response(list(campaigns.values()))
        else:
            campaign = Campaign.objects.get(id=pk)
            
            return Response({
                JSONRenderer().render(CampaignSerializer(campaign).data)
            })
    
    def post(self,request):
        """Recibe datos dentro del request para guardar una nueva Campaign en la base de datos"""
        serializer = self.serializer_class(data=request.data)
        
        if(serializer.is_valid()):
            newCampaign = serializer.create(serializer.validated_data)
            newCampaign.save()

            msg = "Campaign "+newCampaign.name+ " created succesfully"
            # nUser.save()
            return Response({'message':msg})
        else:
            return Response(serializer.errors)

    def put(self,request,pk=None):
        '''Actualiza un objeto con id pk'''
        campaign = Campaign.objects.get(id=pk)
        serializedCampaign = CampaignSerializer(campaign,data=request.data)
        if(serializedCampaign.is_valid()):
            serializedCampaign.save()
            return Response({"message":"PUT funca piola"})
        else:
            return Response(serializedCampaign.errors)

    def patch(self,request,pk=None):
        '''Actualiza valores de un objeto en vez de por completo'''
        user = User.objects.get(id=pk)
        
        msg = "PATCH en objeto con nombre "+user.nombre
        return Response({"message":msg})

    def delete(self,request,pk=None):

        campaign = Campaign.objects.get(id=pk)
        if(campaign == None):
            #TODO: implementar error 404 cdo el objeto no existe
            return Response("")
        campaign.delete()
        msg = "DELETE en objeto con nombre "+campaign.name
        return Response({"message":msg})