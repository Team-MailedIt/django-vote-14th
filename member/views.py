from django.http.response import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.contrib.auth import get_user_model, authenticate
from .models import Candidate, Vote
from .serializers import RegisterSerializer, CandidateSerializer, VoteSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Count

User = get_user_model()

# 회원가입
class RegisterAPIView(APIView):
    def post(self, request):
        user_serializer = RegisterSerializer(data=request.data)
        if user_serializer.is_valid():
            try:
                user = user_serializer.save()
            except:
                return Response(
                    {"message": "email are required!!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
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


class UsernameDuplicateView(APIView):
    def post(self, request):
        username = request.data.get("username")
        isExist = User.objects.filter(username=username).exists()
        return Response(isExist, status=status.HTTP_200_OK)


class EmailDuplicateView(APIView):
    def post(self, request):
        email = request.data.get("email")
        isExist = User.objects.filter(email=email).exists()
        return Response(isExist, status=status.HTTP_200_OK)


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
            return Response(
                {"message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST
            )


class CandidateListAPIView(APIView):
    def get(self, request, format=None):
        candidates = Candidate.objects.all()
        part = request.query_params.get("part", None)
        if part is not None:
            candidates = candidates.filter(part=part)

        # 이름순 정렬
        candidates = candidates.order_by("name")
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class CandidateResultAPIView(APIView):
    def get(self, request, format=None):
        candidates = Candidate.objects.all()
        part = request.GET.get("part", None)
        if part is not None:
            candidates = candidates.filter(part=part)

        # 득표순, 이름순으로 정렬
        candidates = candidates.annotate(vote_count=Count("cand_votes")).order_by(
            "-vote_count", "name"
        )
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class CandidateDetailAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        candidate = self.get_object(pk)
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data, status.HTTP_200_OK)

    # 투표
    def post(self, request, pk, format=None):
        try:
            user = request.user
            candidate = self.get_object(pk)
            vote = Vote(vote_user=user, vote_candidate=candidate)
            vote.save()
            serializer = VoteSerializer(vote)
            return Response(
                {
                    "vote": serializer.data,
                    "message": "Successfully voted",
                },
                status=status.HTTP_200_OK,
            )
        except:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)


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
