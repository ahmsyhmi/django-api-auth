# myapp/urls.py

from django.urls import path
from .views import MyAPIView, MyTokenObtainPairView , CheckUser

urlpatterns = [
    path('checkuser/', CheckUser.as_view()),
    path('myapi/', MyAPIView.as_view()),
    path('token/', MyTokenObtainPairView.as_view()),
]