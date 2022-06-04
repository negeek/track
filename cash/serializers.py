from rest_framework import serializers
from .models import Transaction, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('category_name', 'category_type', 'color')
        model = Category


class TransactionDetailSerializer(serializers.ModelSerializer):
    #owner = serializers.StringRelatedField(many=False)
    category_name = CategorySerializer()

    class Meta:
        fields = ('id', 'owner', 'name', 'amount',
                  'description', 'date_added', 'category_name')
        model = Transaction



