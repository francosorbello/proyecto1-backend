from django.shortcuts import render
from rest_framework import views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.renderers import JSONRenderer
from .models import DonatedElement
from .models import Tag

from DonatedElementAPP.serializers import DonatedElementSerializer
# Create your views here.

class DonatedElementAPPView(APIView):

    serializer_class = DonatedElementSerializer

    def get(self,request,format = None,pk=None):
        '''
        Retorna una lista de Elementos Donados o uno especifico cuando se indica su id.
        
        Parameters
        -----------

        request
            objeto con información de la petición realizada a la API.
        pk: int
            id de un Elemento Donado especifico.
        
        Returns
        ---------

        Response
            Json con una lista de objetos o un objeto individual.
        '''
        if(pk == None):
            delements = DonatedElement.objects.all()
            elements_list = []
            for elem in delements:
                elements_list.append(DonatedElementSerializer(elem).data)
            return Response(elements_list)
        else:
            delement = DonatedElement.objects.get(id=pk)
            return Response(DonatedElementSerializer(delement).data)
    
    def post(self,request):
        """
        Recibe datos dentro del request para guardar un nuevo Elemento Donado en la base de datos.
        
        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.

        Returns
        -------
        
        Response
            JSON con un mensaje de confirmación y el id del nuevo Elemento Donado.
        """
        serializer = self.serializer_class(data=request.data)
        if(serializer.is_valid()):
            newDonatedElement = serializer.create(serializer.validated_data)
            newDonatedElement.save()
            msg = "Donated Element created successfully"
            return Response({'message':msg, "ids":newDonatedElement.id})
        else:
            return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request,pk=None):
        '''
        Actualiza un Elemento Donado con id pk.

        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.
        pk
            id del Elemento Donado a editar

        Returns
        ------
        
        Response
            JSON con un mensaje que indica que el Elemento Donado fue actualizado correctamente
        '''
        delement = DonatedElement.objects.get(id=pk)
        serializedElement = DonatedElementSerializer(delement,data=request.data)
        if(serializedElement.is_valid()):
            serializedElement.save()
            for tag in request.data["tags"]:
                tag_obj = Tag.objects.get(name=tag["name"])
                delement.tags.add(tag_obj)
            
            return Response({"message":"Donated element updated successfully","id":delement.id})
        else:
            return Response(serializedElement.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def patch(self,request,pk=None):
    #     '''Actualiza valores de un objeto en vez de por completo'''
    #     user = User.objects.get(id=pk)
        
    #     msg = "PATCH en objeto con nombre "+user.nombre
    #     return Response({"message":msg})

    def delete(self,request,pk=None):
        """
        Elimina un Elemento Donado de la base de datos.

        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.
        pk
            id del tag a eliminar

        Returns
        --------

        Response
            JSON con mensaje que indica que el Elemento Donado fue creado correctamente.
        """
        delement = DonatedElement.objects.get(id=pk)
        if(delement == None):
            return Response("El elemento donado no existe.",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        delement.delete()
        msg = "Donated Element deleted successfully"
        return Response({"message":msg})