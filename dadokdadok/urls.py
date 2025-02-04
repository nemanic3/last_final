from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # ✅ JWT 관련 추가
from review.views import LikeReviewView
from user.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('book/', include('book.urls')),
    path('review/', include('review.urls')),  # ✅ 단수형으로 변경
    path('goal/', include('goal.urls')),
    path('recommendation/', include('recommendation.urls')),

    # ✅ JWT 로그인 (토큰 발급 및 갱신)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ 리뷰 좋아요 기능 추가
    path('review/<int:review_id>/like/', LikeReviewView.as_view(), name='like_review'),
    path('', home, name='home'),
]
