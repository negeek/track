from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import generics
from .models import Transaction, Category
from .serializers import CategorySerializer, TransactionSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
# Create your views here.


# CATEGORY CREATE UPDATE RETREIVE LIST AND DESTROY VIEWS
class CategoriesView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(owner=user)


class CategoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def retrieve(self, request, id, * args, **kwargs):
        instance = get_object_or_404(Category, id=id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, id, * args, **kwargs):
        instance = get_object_or_404(Category, id=id)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, id,  *args, **kwargs):
        instance = get_object_or_404(Category, id=id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, id, *args, **kwargs):
        return self.retrieve(request, id, *args, **kwargs)

    def patch(self, request, id, *args, **kwargs):
        return self.update(request, id, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()


# TRANSACTION CREATE UPDATE RETREIVE LIST AND DESTROY SVIEWS

class TransactionsView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(owner=user)


class TransactionView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def retrieve(self, request, id, * args, **kwargs):
        instance = get_object_or_404(Transaction, id=id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, id, * args, **kwargs):
        instance = get_object_or_404(Transaction, id=id)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, id,  *args, **kwargs):
        instance = get_object_or_404(Transaction, id=id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, id, *args, **kwargs):
        return self.retrieve(request, id, *args, **kwargs)

    def patch(self, request, id, *args, **kwargs):
        return self.update(request, id, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()

# TRANSACTION FILTERING VIEWS
