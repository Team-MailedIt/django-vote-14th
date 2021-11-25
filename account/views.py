from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

# Create your views here.
class RegisterAPIView(APIView):
    def post(self, request):
        user_serializer = RegisterSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            # access jwt token
            token = TokenObtainPairSerializer.get_token(user)
            return Response(
                {
                    "user": user_serializer.data,
                    "message": "Successfully registered user",
                    "token": {
                        "refresh": str(token),
                        "access": str(token.access_token),
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)