from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from random import choice
from string import digits
# Create your models here.


def generate_random_username(name='nameless', length=5, digits=digits):
    suffix = ''.join([choice(digits) for i in range(length)])
    profile_name = name+suffix

    return profile_name


class CustomUser(AbstractUser):
    phone_number = phone_number = models.CharField(
        max_length=15, help_text='must in clude country code e.g +234-8086235129', blank=True, null=False)
    third_party = models.BooleanField(default=False)


class Profile(models.Model):
    def username(self):
        return self.user.username
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='profile')

    profile_name = models.CharField(
        max_length=100, blank=True)

    avatar = models.FileField(
        default='default.jpg', upload_to='profile_images/')

    def __str__(self):
        return self.user.username
