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
    """
    View del modelo Donation.

    Contiene los métodos para recibir las peticiones REST.

    Attributes
    ---------
    serializer_class
        Serializador del objeto Donation.
    """
    serializer_class = DonationSerializer

    def get(self,request,format = None,pk=None):
        '''
        Retorna una lista de Donaciones o una especifico cuando se indica su id.
        
        Parameters
        -----------

        request
            objeto con información de la petición realizada a la API.
        pk: int
            id de una Donación especifica.
        
        Returns
        ---------

        Response
            Json con una lista de objetos o un objeto individual.
        '''
        if(pk == None):
            donations = Donation.objects.all()
            serializedDonations = DonationSerializer(donations,many=True)
            return Response(serializedDonations.data)
        else:
            donation = Donation.objects.get(id=pk)
            serialDonation = DonationSerializer(donation)
            return Response(serialDonation.data)
    
    def post(self,request):
        """
        Recibe datos dentro del request para guardar una nueva Donacion en la base de datos.
        
        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.

        Returns
        -------
        
        Response
            JSON con un mensaje de confirmación, el id de la nueva Donación y una lista
            de ids de los nuevos Elementos Donados.
        """
        serializer = self.serializer_class(data=request.data)
        if(serializer.is_valid()):
            newDonation = serializer.create(serializer.validated_data)
            newDonation.save()
            donatedElemIds = []
            donatedElems = DonatedElement.objects.filter(donation=newDonation.id)
            for elem in donatedElems:
                donatedElemIds.append(elem.id)
            msg = "Donation created successfully"
            return Response({'message':msg,'id':newDonation.id,'donatedElemIds':donatedElemIds})
        else:
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request,pk=None):
        '''
        Actualiza una Donación con id pk.

        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.
        pk
            id de la Donación a editar.

        Returns
        ------
        
        Response
            JSON con un mensaje que indica que la Donación fue actualizada correctamente.
        '''
        donation = Donation.objects.get(id=pk)
        serializedDonation = DonationSerializer(donation,data=request.data)
        if(serializedDonation.is_valid()):
            serializedDonation.save()
        else:
            return Response(serializedDonation.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self,request,pk=None):
        '''
        Actualiza una Donación con id pk.

        A diferencia del put, la información dentro de request puede ser parcial, 
        es decir, no tener todos los campos del objeto.

        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.
        pk
            id de la Donación a editar.

        Returns
        ------
        
        Response
            JSON con un mensaje que indica que la Donación fue actualizada correctamente.
        '''
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
        """
        Elimina una Donación de la base de datos.

        Eliminar una Donación también borrará las donaciones (y elementos donados) asociadas.

        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.
        pk
            id de la Donación a eliminar

        Returns
        --------

        Response
            JSON con mensaje que indica que la Donación fue eliminada correctamente.
        """
        donation = Donation.objects.get(id=pk)
        if(donation == None):
            #TODO: implementar error 404 cdo el objeto no existe
            return Response("")
        donation.delete()
        msg = "Donation deleted successfully"
        return Response({"message":msg})