from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    CASH_FLOW = [('debit', 'debit'),
                 ('credit', 'credit')]
    category_type = models.CharField(max_length=20,
                                     choices=CASH_FLOW,
                                     default='debit')
    category_name = models.CharField(max_length=25)
    color = models.CharField(max_length=25)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class Transaction(models.Model):
    name = models.CharField(max_length=25)
    category_name = models.OneToOneField(
        Category, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    description = models.TextField(blank=True, default='')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
