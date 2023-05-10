from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.generics import CreateAPIView
from .serializers import *

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class RefreshAPIView(APIView):
    def post(self, request):
        refresh = request.data.get('refresh')
        try:
            token = RefreshToken(refresh)
            token.blacklist()
            new_refresh = RefreshToken.for_user(token.user)
            return Response({
                'refresh': str(new_refresh),
                'access': str(new_refresh.access_token)
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SnippetCreateView(CreateAPIView):
    def post(self, request):
        serializer = SnippetCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class DeleteSnippet(APIView):
    def get(self,request,id):
        if id is not None:
            question1      = Snippet.objects.get(id=id)
            serializer     = VSnippetSerializer(question1)
            return Response(serializer.data) 
        question1      = Snippet.objects.all()       
        serializer     = VSnippetSerializer(question1,many=True)
        return Response(serializer.data)
    def delete(self,req,id):

        Snippet.objects.get(id=id).delete()
        return Response({"msg":1}) 
        
class SnippetList(generics.ListAPIView):
    queryset = Snippet.objects.all()
    serializer_class = LSnippetSerializer

    def get(self, request, *args, **kwargs):
        snippets = self.get_queryset()
        serializer = self.get_serializer(snippets, many=True)
        count = snippets.count()
        data = {
            'count': count,
            'snippets': serializer.data,
        }
        for snippet in data['snippets']:
            snippet['url'] = reverse('detail', args=[snippet['id']], request=request)
        return Response(data)
    
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = LSnippetSerializer

class TagList(APIView):
    def get(self,request):
        tag = Tag.objects.all()
        serializer = LTagSerializer(tag,many=True)
        return Response(serializer.data)

class TagDetails(APIView):
    def post(self,request):
        tag = request.data['tag']
        snippet=Snippet.objects.filter(tag=tag)
        serializer = LSnippetSerializer(snippet,many=True)
        return Response(serializer.data)