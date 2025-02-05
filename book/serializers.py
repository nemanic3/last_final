from rest_framework import serializers
from .models import Book
from review.models import Review

class BookSerializer(serializers.ModelSerializer):
    """ DB에 저장된 책 정보를 직렬화 """
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'publisher', 'image_url', 'created_at']

class NaverBookSerializer(serializers.Serializer):
    """ 네이버 API 검색 결과 직렬화 (DB 저장 안 함) """
    title = serializers.CharField()
    author = serializers.CharField()
    publisher = serializers.CharField()
    published_date = serializers.CharField(source='pubdate')
    isbn = serializers.CharField()
    image_url = serializers.URLField(source='image')
    link = serializers.URLField()

class BookWithReviewSerializer(serializers.ModelSerializer):
    """ 최신 리뷰 포함된 책 정보 직렬화 """
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'publisher', 'image_url', 'created_at', 'reviews']

    def get_reviews(self, obj):
        reviews = Review.objects.filter(book=obj).order_by('-created_at')[:5]  # 최신 리뷰 5개 가져오기
        return [{"id": r.id, "user": r.user.username, "rating": r.rating, "content": r.content} for r in reviews]
