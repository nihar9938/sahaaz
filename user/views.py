from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class HelloWorld(APIView):
    @staticmethod
    def get(self):
        return Response({'Hi': 'Welcome'})
