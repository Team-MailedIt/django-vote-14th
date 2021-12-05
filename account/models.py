from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

PART_CHOICES = [
    ("FE", "프론트엔드"),
    ("BE", "백엔드"),
]


class User(AbstractUser):
    part = models.CharField(max_length=2, choices=PART_CHOICES)


class Candidate(models.Model):
    name = models.CharField(max_length=30)
    part = models.CharField(max_length=2, choices=PART_CHOICES)

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
