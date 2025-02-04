from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, LikeReviewView, CommentView

router = DefaultRouter()
router.register('', ReviewViewSet, basename='review')

urlpatterns = [
    path('<int:review_id>/like/', LikeReviewView.as_view(), name='like_review'),
    path('<int:review_id>/comment/', CommentView.as_view(), name='comment_review'),
]

urlpatterns += router.urls