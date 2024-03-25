# myapp/views.py

from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework import status, throttling
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsSuperUser

class CheckUser(APIView):
    permission_classes = [IsAuthenticated],[IsSuperUser]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method == 'GET':
            return [IsAuthenticated(), IsSuperUser()]
        else:
            return []

    def get(self, request):
        self.name = request.user.username
        content = {'message': 'Hello, ' + self.name + '!'}
        return Response(content)

class MyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        self.name = request.user.username
        content = {'message': 'Hello, ' + self.name + '!'}
        return Response(content)

class MyTokenObtainPairView(APIView):
    throttle_classes = [throttling.AnonRateThrottle]
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Authentication successful, generate JWT tokens
            token = RefreshToken.for_user(user)
            return Response({"token": str(token.access_token)}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
