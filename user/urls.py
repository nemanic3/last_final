from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SignupView, LoginView, LogoutView
from django.http import JsonResponse

router = DefaultRouter()
router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]

