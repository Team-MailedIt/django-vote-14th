from django.http.response import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.contrib.auth import get_user_model, authenticate
from .models import Candidate, Vote
from .serializers import RegisterSerializer, CandidateSerializer, VoteSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated


User = get_user_model()

# 회원가입
class RegisterAPIView(APIView):
    def post(self, request):
        user_serializer = RegisterSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            # access jwt token
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": user_serializer.data,
                    "message": "Successfully registered user",
                    "token": {
                        "refresh": refresh_token,
                        "access": access_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인
class AuthView(APIView):
    # 유저정보 확인
    def get(self, request):
        pass

    # 로그인
    def post(self, request):
        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
        )
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": {
                        "username": user.username,
                        "password": user.password,
                        "part": user.part,
                    },
                    "message": "Successfully logged in",
                    "token": {
                        "refresh": refresh_token,
                        "access": access_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CandidateListAPIView(APIView):
    def get(self, request, format=None):
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class CandidateDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        candidate = self.get_object(pk)
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data, status.HTTP_200_OK)


class VoteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            user_id = request.data.get("user_id")
            candidate_id = request.data.get("candidate_id")
            vote = Vote.objects.create(
                vote_user=User.objects.get(pk=user_id),
                vote_candidate=Candidate.objects.get(pk=candidate_id),
            )
            serializer = VoteSerializer(vote)
        except Exception:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status.HTTP_201_CREATED)


class TestAPIView(APIView):
    def get(self, request):
        return Response(
            {"message": "test API successfully responsed"}, status=status.HTTP_200_OK
        )


# 로그인했을 때만 가능한 요청
class TestAuthAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        return Response(
            {"message": "test Auth API successfully responsed"},
            status=status.HTTP_200_OK,
        )
