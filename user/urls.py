from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SignupView, LoginView, LogoutView

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),  # ✅ 회원가입 (POST)
    path('login/', LoginView.as_view(), name='login'),  # ✅ 로그인 (POST, JWT 발급)
    path('logout/', LogoutView.as_view(), name='logout'),  # ✅ 로그아웃 (POST)
    path('', include(router.urls)),  # ✅ ViewSet 추가
]
