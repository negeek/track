from rest_framework import serializers
from .models import Transaction, Category, Budget
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
                  'amount', 'time_of_transaction', 'budget_id', 'owner')
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
        instance.budget_id = validated_data.get(
            'budget_id', instance.budget_id)
        instance.save()
        return instance


class CategoryDBSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('category_name', 'category_type')
        model = Category


class TransactionFilterSerializer(serializers.ModelSerializer):
    category_id = CategoryDBSerializer()

    class Meta:
        fields = ('id', 'name', 'amount',
                  'description', 'time_of_transaction', 'category_id')
        model = Transaction


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'amount', 'start_date', 'to_date', 'active', 'owner')
        read_only_fields = ('start_date',)
        model = Budget

    def create(self, validated_data):
        return Budget.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get(
            'amount', instance.amount)
        instance.start_date = validated_data.get(
            'start_date', instance.start_date)
        instance.to_date = validated_data.get(
            'to_date', instance.to_date)
        instance.active = validated_data.get(
            'active', instance.active)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance
