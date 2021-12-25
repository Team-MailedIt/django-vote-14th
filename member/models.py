from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.

PART_CHOICES = [
    ("frontend", "frontend"),
    ("backend", "backend"),
]


class User(AbstractUser):
    part = models.CharField(max_length=10, choices=PART_CHOICES)

    objects = UserManager()
    REQUIRED_FIELDS = ["email"]


class Candidate(models.Model):
    name = models.CharField(max_length=10)
    part = models.CharField(max_length=10, choices=PART_CHOICES)

    def __str__(self):
        return self.name


class Vote(models.Model):
    vote_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_votes"
    )
    vote_candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="cand_votes"
    )

    def __str__(self):
        return f"{self.vote_user.username}'s vote on {self.vote_candidate.name}"
