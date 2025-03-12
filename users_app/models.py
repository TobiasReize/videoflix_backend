from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    custom = models.TextField(max_length=500, default='', blank=True)
    address = models.CharField(max_length=150, default='', blank=True)
    phone = models.CharField(max_length=25, default='', blank=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username
