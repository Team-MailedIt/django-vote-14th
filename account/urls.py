from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    # path("signin", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # 세션 연장하고 싶을 때 refresh token 사용
    # path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("signin", AuthView.as_view()),
    path("signup", RegisterAPIView.as_view()),
    path("candidate", CandidateListAPIView.as_view()),
    path("candidate/result", CandidateResultAPIView.as_view()),
    path("candidate/<int:pk>", CandidateDetailAPIView.as_view()),
    path("test", TestAPIView.as_view()),
    path("testauth", TestAuthAPIView.as_view()),
]
