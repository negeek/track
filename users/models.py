from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    phone_number = phone_number = models.CharField(
        max_length=15, help_text='must in clude country code e.g +234-8086235129', blank=True, null=False)
    third_party = models.BooleanField(default=False)
