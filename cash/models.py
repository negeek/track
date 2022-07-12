from django.utils import timezone
from django.forms import DateInput
from datetime import date
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.


class Category(models.Model):
    CASH_FLOW = [('debit', 'debit'),
                 ('credit', 'credit')]
    category_type = models.CharField(max_length=20,
                                     choices=CASH_FLOW,
                                     default='debit')
    category_name = models.CharField(max_length=25)
    description = models.TextField(blank=True, default='')
    color = models.CharField(max_length=25)

    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True)
    icon = models.CharField(max_length=25, default='')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class Budget(models.Model):
    amount = models.FloatField(default=0.0)
    start_date = models.DateField(default=date.today())
    to_date = models.DateField(default=date.today())
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    name = models.CharField(max_length=25)
    category_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True)
    budget_id = models.ForeignKey(Budget, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(default=0.0)

    description = models.TextField(default='')
    time_of_transaction = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
