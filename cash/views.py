from rest_framework import mixins, views
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import generics
from .models import Transaction, Budget
from .serializers import CategorySerializer, TransactionFilterSerializer, TransactionSerializer, BudgetSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date

from rest_framework.permissions import IsAuthenticated
# Create your views here.


# CATEGORY CREATE UPDATE RETREIVE LIST AND DESTROY VIEWS
class CategoriesView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(owner=user).order_by('category_name')


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
        return Transaction.objects.filter(owner=user).order_by('-time_of_transaction')


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


class DebitCreditView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, transaction_type):
        transactions = Transaction.objects.filter(
            owner=request.user).order_by('-time_of_transaction')
        serializer = TransactionFilterSerializer(transactions, many=True)
        result = []
        for data in serializer.data:
            if data['category_id']['category_type'] == transaction_type:
                result.append(data)
        return Response(result)


class DateFilterView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, start_year, start_month, start_day, end_year=None, end_month=None, end_day=None):
        if not end_year and not end_month and not end_day:
            end_year, end_month, end_day = date.today(
            ).year, date.today().month, date.today().day
            end_date = date(end_year, end_month, end_day)
        else:
            end_date = date(end_year, end_month, end_day)

        start_date = date(start_year, start_month, start_day)

        transactions = Transaction.objects.filter(
            owner=request.user, time_of_transaction__range=(
                start_date, end_date)).order_by('-time_of_transaction')
        serializer = TransactionFilterSerializer(transactions, many=True)
        return Response(serializer.data)

# BUDGET


class BudgetsView(generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        return Budget.objects.filter(owner=user, active=True)


class BudgetStatus(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        if self.budget_isactive(id):
            transactions = Transaction.objects.filter(
                owner=request.user, budget_id=id)
            total_expense = 0
            serializer = TransactionFilterSerializer(transactions, many=True)
            for data in serializer.data:
                if data['category_id']['category_type'] == 'debit':
                    total_expense += data['amount']
            budget = get_object_or_404(Budget, id=id)
            balance = (budget.amount)-total_expense
            duration = budget.to_date-budget.start_date
            days_elapsed = date.today()-budget.start_date
            result = {'budget': budget.amount, 'balance': balance,
                      'date_elapsed': days_elapsed.days, 'budget_period': duration.days}
            return Response(result)
        else:
            result = {'budget': 0, 'balance': 0, 'duration': 0}
            return Response(result)

    def budget_isactive(self, id):
        today = date.today()
        budget = Budget.objects.get(id=id)
        if today > budget.to_date:
            budget['active'] = False
            budget.save()
            return False
        return True


class BudgetView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BudgetSerializer

    def retrieve(self, request, id, * args, **kwargs):
        self.check_active_budgets()
        instance = get_object_or_404(Budget, id=id)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, id, * args, **kwargs):
        instance = get_object_or_404(Budget, id=id)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, id,  *args, **kwargs):
        instance = get_object_or_404(Budget, id=id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, id, *args, **kwargs):
        return self.retrieve(request, id, *args, **kwargs)

    def patch(self, request, id, *args, **kwargs):
        return self.update(request, id, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()
