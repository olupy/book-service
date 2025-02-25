from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,  OrderingFilter
from library.models import Book
from library.v1.serializers import BookSerializer, BorrowBookSerializer
from library.models import Borrow


# Create your views here.

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ["get", "post"]
    search_fields = ["title", "author", "isbn"]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = ["genre", "language", "sub_category", "publisher"]


class BorrowBookViewSet(ModelViewSet):
    queryset = Borrow.objects.all().select_related("book", "user")
    serializer_class = BorrowBookSerializer
    http_method_names = ["get"]
    search_fields = ["book__title", "book__author", "user__firstname","user__lastname"]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = ["is_returned","is_overdue"]



