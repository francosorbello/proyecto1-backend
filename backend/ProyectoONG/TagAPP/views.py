from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.renderers import JSONRenderer
from .models import Tag

from TagAPP.serializers import TagSerializer
# Create your views here.

class TagAPPView(APIView):

    serializer_class = TagSerializer

    def get(self,request,format = None,pk=None):
        '''retorna una lista de tags o uno especifico cuando se indica su id'''
        if(pk == None):
            tags = Tag.objects.all()
            return Response(list(tags.values()))
        else:
            tag = Tag.objects.get(id=pk)
            return Response(TagSerializer(tag).data)
    
    def post(self,request):
        """Recibe datos dentro del request para guardar un nuevo Tag en la base de datos"""
        serializer = self.serializer_class(data=request.data)
        
        if(serializer.is_valid()):
            tagName = serializer.validated_data.get("name")
            if Tag.objects.filter(name=tagName).exists():
                #TODO: añadir error correcto
                return Response({'message': "El tag ya existe"})
            else:
                newTag = serializer.create(serializer.validated_data)
                newTag.save()
                msg = "Tag "+newTag.name+ " created succesfully"
                return Response({'message':msg})
        else:
            return Response(serializer.errors)

    def put(self,request,pk=None):
        '''Actualiza un objeto con id pk'''
        tag = Tag.objects.get(id=pk)
        serializedTag = TagSerializer(tag,data=request.data)
        if(serializedTag.is_valid()):
            serializedTag.save()
            return Response({"message":"PUT funca piola"})
        else:
            return Response(serializedTag.errors)

    # def patch(self,request,pk=None):
    #     '''Actualiza valores de un objeto en vez de por completo'''
    #     user = User.objects.get(id=pk)
        
    #     msg = "PATCH en objeto con nombre "+user.nombre
    #     return Response({"message":msg})

    def delete(self,request,pk=None):

        tag = Tag.objects.get(id=pk)
        if(tag == None):
            #TODO: implementar error 404 cdo el objeto no existe
            return Response("")
        tag.delete()
        msg = "DELETE en objeto con nombre "+tag.name
        return Response({"message":msg})