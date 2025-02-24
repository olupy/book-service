from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
# Create your views here.
from user.models import User
from .serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get','put',]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    search_fields = ['email', 'firstname', 'lastname']
    filterset_fields = ['email', 'firstname', 'lastname']
