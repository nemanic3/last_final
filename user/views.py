from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .serializers import SignupSerializer, UserSerializer

User = get_user_model()


# ✅ API 상태 확인용 홈 뷰 (함수형 뷰로 변경 가능)
def home(request):
    """API 서버 상태 확인"""
    return JsonResponse({"message": "DadokDadok API is running!"})


# ✅ 회원가입 API
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Signup successful!",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
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
        return Response({
            "message": "Login successful!",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)


# ✅ 로그아웃 API (JWT 토큰 블랙리스트 적용 가능)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


# ✅ 회원 정보 조회, 수정 API
class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path='me')
    def me(self, request):
        """사용자 정보 조회"""
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=["put"], url_path='update-profile')
    def update_profile(self, request):
        """사용자 프로필 수정 (닉네임 중복 검사 추가 가능)"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully.",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
