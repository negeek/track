from django.shortcuts import render
from rest_framework import generics
from .models import Transaction, Category
from .serializers import TransactionDetailSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

'''
class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    '''


@api_view(['GET'])
def TransactionDetail(request):
    if request.method == 'GET':

        print(len(request.GET))
        owner = request.GET['owner']
        transaction = Transaction.objects.filter(owner=owner)
        serializer = TransactionDetailSerializer(transaction, many=True)
        serializer_data = serializer.data
        if len(request.GET) > 1:
            category_type = request.GET['category_type']
            for data in serializer_data:
                if data['category_name']['category_type'] != category_type:
                    serializer_data.remove(data)

        return Response(serializer_data)
