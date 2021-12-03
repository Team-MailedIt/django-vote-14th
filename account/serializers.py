from django.db.models.base import Model
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Candidate, Vote

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "part")

    def create(self, validated_data):
        user = User(
            username=validated_data.get("username"),
            part=validated_data.get("part"),
        )
        user.set_password(validated_data.get("password"))
        user.save()
        return user


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["id", "name", "part"]


class VoteSerializer(serializers.ModelSerializer):
    vote_user = serializers.SerializerMethodField()
    vote_candidate = serializers.SerializerMethodField()

    def get_vote_user(self, obj):
        return obj.vote_user.username

    def get_vote_candidate(self, obj):
        return obj.vote_candidate.name

    class Meta:
        model = Vote
        fields = ["id", "vote_user", "vote_candidate"]
