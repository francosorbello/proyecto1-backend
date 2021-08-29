from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.renderers import JSONRenderer
from .models import User

from UserAPP.serializers import UserSerializer
# Create your views here.

class UserAPPView(APIView):

    serializer_class = UserSerializer

    def get(self,request,format = None,pk=None):
        '''retorna una lista de users o uno especifico cuando se indica su id'''
        if(pk == None):
            users = User.objects.all()
            return Response(list(users.values()))
        else:
            user = User.objects.get(id=pk)
            
            #TODO: revisar esto
            return Response({
                JSONRenderer().render(UserSerializer(user).data)
            })
    
    def post(self,request):
        """Recibe datos dentro del request para guardar un nuevo User en la base de datos"""
        serializer = self.serializer_class(data=request.data)
        
        if(serializer.is_valid()):
            userMail = serializer.validated_data.get("mail")
            if User.objects.filter(mail=userMail).exists():
                #TODO: añadir error correcto
                return Response({'message': "El mail pertenece a un usuario previamente registrado"})
            else:
                newUser = serializer.create(serializer.validated_data)
                newUser.save()
                msg = "User "+newUser.name+ " created succesfully"
                return Response({'message':msg})
        else:
            return Response(serializer.errors)

    def put(self,request,pk=None):
        '''Actualiza un objeto con id pk'''
        user = User.objects.get(id=pk)
        serializedUser = UserSerializer(user,data=request.data)
        if(serializedUser.is_valid()):
            serializedUser.save()
            return Response({"message":"PUT funca piola"})
        else:
            return Response(serializedUser.errors)

    # def patch(self,request,pk=None):
    #     '''Actualiza valores de un objeto en vez de por completo'''
    #     user = User.objects.get(id=pk)
        
    #     msg = "PATCH en objeto con nombre "+user.nombre
    #     return Response({"message":msg})

    def delete(self,request,pk=None):

        user = User.objects.get(id=pk)
        if(user == None):
            #TODO: implementar error 404 cdo el objeto no existe
            return Response("")
        user.delete()
        msg = "DELETE en objeto con nombre "+user.name
        return Response({"message":msg})