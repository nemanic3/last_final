from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .serializers import UserSerializer, SignupSerializer
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

User = get_user_model()

# ✅ 홈 API 추가
def home(request):
    return JsonResponse({"message": "Welcome to DadokDadok API!"})

# ✅ 회원가입 API
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(password=make_password(serializer.validated_data['password']))
            return Response({"message": "Signup successful!", "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ 로그인 API (JWT 인증)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({"message": "Login successful!", "token": str(refresh.access_token)}, status=status.HTTP_200_OK)

# ✅ 로그아웃 API (JWT는 클라이언트에서 삭제하는 방식)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

# ✅ 회원 정보 조회 및 삭제 API
class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def me(self, request):
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=["delete"])
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "Account successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
