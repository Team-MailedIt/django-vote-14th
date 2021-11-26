from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

PART_CHOICES = [
    ("FE", "프론트엔드"),
    ("BE", "백엔드"),
]


class User(AbstractUser):
    part = models.CharField(max_length=2, choices=PART_CHOICES)
