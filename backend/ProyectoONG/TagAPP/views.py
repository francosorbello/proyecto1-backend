from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.renderers import JSONRenderer
from .models import Tag

from TagAPP.serializers import TagSerializer
# Create your views here.

class TagAPPView(APIView):
    """
    View del modelo Tag.

    Contiene los métodos para recibir las peticiones REST.

    Attributes
    ---------
    serializer_class
        Serializador del objeto Tag.
    """
    
    serializer_class = TagSerializer

    def get(self,request,format = None,pk=None):
        '''
        Retorna una lista de tags o uno especifico cuando se indica su id.
        
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
            tags = Tag.objects.all()
            return Response(list(tags.values()))
        else:
            tag = Tag.objects.get(id=pk)
            return Response(TagSerializer(tag).data)
    
    def post(self,request):
        """
        Recibe datos dentro del request para guardar un nuevo Tag en la base de datos.
        
        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.

        Returns
        -------
        
        Response
            JSON con un mensaje de confirmación y el id del nuevo Tag
        """
        serializer = self.serializer_class(data=request.data)
        
        if(serializer.is_valid()):
            tagName = serializer.validated_data.get("name")
            if Tag.objects.filter(name=tagName).exists():
                return Response({"message":"El tag solicitado ya existe"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                newTag = serializer.create(serializer.validated_data)
                newTag.save()
                msg = "Tag "+newTag.name+ " created successfully"
                return Response({'message':msg,"id":newTag.id})
        else:
            return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request,pk=None):
        '''
        Actualiza un tag con id pk.

        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.
        pk
            id del tag a editar

        Returns
        ------
        
        Response
            JSON con un mensaje que indica que el tag fue actualizado correctamente
        '''
        tag = Tag.objects.get(id=pk)
        serializedTag = TagSerializer(tag,data=request.data)
        if(serializedTag.is_valid()):
            serializedTag.save()
            return Response({"message":"Tag updated successfully"})
        else:
            return Response(serializedTag.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def patch(self,request,pk=None):
    #     '''Actualiza valores de un objeto en vez de por completo'''
    #     user = User.objects.get(id=pk)
        
    #     msg = "PATCH en objeto con nombre "+user.nombre
    #     return Response({"message":msg})

    def delete(self,request,pk=None):
        """
        Elimina un tag de la base de datos.

        Parameters
        ----------
        
        request
            objeto con información de la petición realizada a la API.
        pk
            id del tag a eliminar

        Returns
        --------

        Response
            JSON con mensaje que indica que el tag fue creado correctamente.
        """
        tag = Tag.objects.get(id=pk)
        if(tag == None):
            return Response({"message":"El tag solicitado no existe"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        tag.delete()
        msg = "Tag "+tag.name+" deleted successfully"
        return Response({"message":msg})