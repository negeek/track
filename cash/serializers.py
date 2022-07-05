from rest_framework import serializers
from .models import Transaction, Category
from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        fields = ('id', 'category_name',
                  'description', 'category_type', 'color', 'icon', 'owner')
        model = Category

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get(
            'category_name', instance.category_name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.category_type = validated_data.get(
            'category_type', instance.category_type)
        instance.color = validated_data.get('color', instance.color)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'description', 'category_id',
                  'amount', 'time_of_transaction', 'owner')
        model = Transaction

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.category_id = validated_data.get(
            'category_id', instance.category_id)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.time_of_transaction = validated_data.get(
            'time_of_transaction', instance.time_of_transaction)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance


class CategoryDBSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('category_name', 'category_type')
        model = Category


class TransactionDBSerializer(serializers.ModelSerializer):
    category_id = CategoryDBSerializer()

    class Meta:
        fields = ('id', 'name', 'amount',
                  'description', 'time_of_transaction', 'category_id')
        model = Transaction
