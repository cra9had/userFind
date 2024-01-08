from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    available_searches = models.IntegerField(default=0, verbose_name="Search available")
    avatar = models.ImageField(default='profiles/default.png', verbose_name="User avatar", upload_to='profiles/')
