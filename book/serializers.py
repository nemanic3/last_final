from rest_framework import serializers
from .models import Book
from review.models import Review

class BookSerializer(serializers.ModelSerializer):
    """
    DB에 저장된 책 정보를 직렬화
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'publisher', 'image_url', 'created_at']

class NaverBookSerializer(serializers.Serializer):
    """
    네이버 API 검색 결과를 위한 직렬화 클래스 (DB 저장 안 함)
    """
    title = serializers.CharField()
    author = serializers.CharField()
    publisher = serializers.CharField()
    pubdate = serializers.CharField()
    isbn = serializers.CharField()
    image = serializers.URLField(source='image_url')
    link = serializers.URLField()

class BookWithReviewSerializer(serializers.ModelSerializer):
    """
    최근 리뷰가 포함된 책 정보 직렬화
    """
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'publisher', 'image_url', 'created_at', 'reviews']

    def get_reviews(self, obj):
        reviews = Review.objects.filter(book=obj).order_by('-created_at')[:5]  # 최신 리뷰 5개 가져오기
        return [{"id": r.id, "user": r.user.username, "rating": r.rating, "content": r.content} for r in reviews]
