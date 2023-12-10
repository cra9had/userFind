from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    balance = models.IntegerField(default=0, verbose_name="Balance")
    avatar = models.ImageField(default='profiles/default.png', verbose_name="User avatar", upload_to='profiles/')
