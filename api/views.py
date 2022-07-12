from django.shortcuts import render
from rest_framework.views import APIView
from api.models import Todos
from rest_framework.response import Response
from api.serializers import TodoSerializer,UserSerializer,LoginSerializer
from rest_framework import status
from django.contrib.auth import authenticate,login
from rest_framework import authentication,permissions
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework import serializers
from rest_framework.viewsets import ViewSet,ModelViewSet
# Create your views here.



class TodosView(APIView):
    authentication_classes = [authentication.BasicAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        qs=Todos.objects.filter(user=request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        serializer=TodoSerializer(data=request.data,context={'user':request.user})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class TodoDEtails(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("todo_id")
        todo=Todos.objects.get(id=id)
        serializer=TodoSerializer(todo)
        return Response(serializer.data)

    def put(self,request,*args,**kwargs):
        id=kwargs.get("todo_id")
        todo=Todos.objects.get(id=id)
        serializer=TodoSerializer(instance=todo,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("todo_id")
        todo=Todos.objects.get(id=id)
        todo.delete()
        return Response({"msg":"deleted"})




#blog(id,title,content,author)
#api


class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SignINView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            uname=serializer.validated_data.get("username")
            passw=serializer.validated_data.get("password")
            user=authenticate(request,username=uname,password=passw)
            if user:
                login(request,user)
                return Response({"msg":"sucess"})
            else:
                return Response({"msg":"invalid credentials"})


#master_string="abbegddct"
#check_str="egg"

class TodosMixinView(GenericAPIView,
                     ListModelMixin,
                     CreateModelMixin):
    serializer_class = TodoSerializer
    queryset = Todos.objects.all()
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class TodomixDetailsView(GenericAPIView,
                         RetrieveModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin):
    serializer_class = TodoSerializer
    queryset = Todos.objects.all()
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg ="todo_id"

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def perform_destroy(self, instance):
        if instance.user==self.request.user:   #this is known the user owner todos
            instance.delete()
        else:
            raise serializers.ValidationError("Not allowed")
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


#viewsets
class TodosViewsetView(ViewSet):
    model = Todos
    serializers_class = TodoSerializer
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        qs = Todos.objects.filter(user=request.user)
        serializer = self.serializers_class(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializers_class(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        todos = Todos.objects.get(id=id)
        serializer = self.serializers_class(todos)
        return Response(serializer.data)

    def update(self,request,*args,**kwargs):
        print(kwargs)
        id=kwargs.get("pk")
        todos=Todos.objects.get(id=id)
        serializer=self.serializers_class(instance=todos,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo=Todos.objects.get(id=id)
        todo.delete()
        return Response({"msg":"deleted"})

class TodoModelViewsetView(ModelViewSet):
    # authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model=Todos
    serializer_class = TodoSerializer
    queryset = Todos.objects.all()

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.serializers_class(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)



