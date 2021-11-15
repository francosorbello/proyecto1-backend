
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
        '''
        Retorna una lista de campañas o una especifica cuando se indica su id.

        Si el request contiene un atributo "onlyActive" y éste es verdadero, sólo se
        retornan aquellas campañas cuya fecha de fin sea mayor a la fecha actual.
        
        Parameters
        -----------

        request
            objeto con información de la petición realizada a la API.
        pk: int
            id de un tag especifico.
        
        Returns
        ---------

        Response
            Json con una lista de objetos o un objeto individual.
        '''
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
        """
        Recibe datos dentro del request para guardar una nueva campaña en la base de datos.

        Si la fecha de inicio es mayor a la fecha de fin, retorna error 500.
        
        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.

        Returns
        -------
        
        Response
            JSON con un mensaje de confirmación y el id de la nueva campaña
        """
        serializer = self.serializer_class(data=request.data)
        
        if(serializer.is_valid()):
            newCampaign = serializer.create(serializer.validated_data)

            if(newCampaign.initialDate > newCampaign.endDate):
                return Response({'message': "La fecha de inicio es posterior a la de fin"},status=status.HTTP_400_BAD_REQUEST)

            newCampaign.save()

            msg = "Campaign "+newCampaign.name+ " created successfully"
            return Response({'message':msg,"id":newCampaign.id})
        else:
            return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request,pk=None):
        '''
        Actualiza una campaña con id pk.

        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.
        pk
            id de la campaña a editar

        Returns
        ------
        
        Response
            JSON con un mensaje que indica que la campaña fue actualizada correctamente
        '''
        campaign = Campaign.objects.get(id=pk)
        serializedCampaign = CampaignSerializer(campaign,data=request.data)
        if(serializedCampaign.is_valid()):
            serializedCampaign.save()
            return Response({"message":"Campaign updated successfully"})
        else:
            return Response(serializedCampaign.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self,request,pk=None):
        '''
        Actualiza una campaña con id pk.

        A diferencia del put, la información dentro de request puede ser parcial, 
        es decir, no tener todos los campos del objeto.

        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.
        pk
            id de la Campaña a editar.

        Returns
        ------
        
        Response
            JSON con un mensaje que indica que la Campaña fue actualizada correctamente.
        '''
        campaign = Campaign.objects.get(id=pk)
        serializedCampaign = CampaignSerializer(campaign,data=request.data,partial=True)
        if(serializedCampaign.is_valid()):
            serializedCampaign.save()
            return Response({"message":"Campaign updated successfully"})
        else:
            return Response(serializedCampaign.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,pk=None):
        """
        Elimina una campaña de la base de datos.

        Eliminar una campaña también borrará las donaciones (y elementos donados) asociadas.

        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.
        pk
            id de la campaña a eliminar

        Returns
        --------

        Response
            JSON con mensaje que indica que la campaña fue eliminada correctamente.
        """
        campaign = Campaign.objects.get(id=pk)
        if(campaign == None):
            return Response({"message":"La campaña que deseas borrar no existe"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        campaign.delete()
        msg = "Campaign "+campaign.name+ " deleted successfully"
        return Response({"message":msg})