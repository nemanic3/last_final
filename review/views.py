from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from .models import Review, Like, Comment
from book.models import Book
from .serializers import ReviewSerializer, LikeSerializer, CommentSerializer
from book.services import get_book_by_isbn_from_naver

class ReviewViewSet(viewsets.ModelViewSet):
    """ 리뷰 CRUD 기능 제공 """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """ 리뷰 작성 시 `isbn`을 받아서 책을 조회/생성 후 리뷰 저장 """
        isbn = self.request.data.get("isbn")
        if not isbn:
            raise ValidationError({"isbn": "ISBN이 필요합니다."})

        book = Book.objects.filter(isbn=isbn).first()

        if not book:
            book_data = get_book_by_isbn_from_naver(isbn)
            if not book_data:
                raise ValidationError({"isbn": "해당 ISBN으로 책 정보를 찾을 수 없습니다."})

            book = Book.objects.create(
                isbn=isbn,
                title=book_data.get("title", "Unknown Title"),
                author=book_data.get("author", "Unknown Author"),
                publisher=book_data.get("publisher", "Unknown Publisher"),
                published_date=book_data.get("pubdate", ""),
                image_url=book_data.get("image", ""),
            )
        serializer.context['book'] = book
        serializer.save(user=self.request.user)


class LikeReviewView(APIView):
    """ 리뷰 좋아요 기능 """
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        review = Review.objects.filter(id=review_id).first()
        if not review:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, review=review)

        if not created:
            like.delete()
            return Response({"message": "Like removed", "likes_count": review.likes.count()}, status=status.HTTP_200_OK)

        return Response({"message": "Like added", "likes_count": review.likes.count()}, status=status.HTTP_201_CREATED)


class CommentView(APIView):
    """ 댓글 작성 기능 """
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        review = Review.objects.filter(id=review_id).first()
        if not review:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "user": request.user.id,
            "review": review.id,
            "content": request.data.get("content")
        }
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListView(APIView):
    """ 특정 리뷰의 댓글 목록 조회 기능 """
    permission_classes = [AllowAny]

    def get(self, request, review_id):
        comments = Comment.objects.filter(review_id=review_id).order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecentReviewView(APIView):
    """ 최신 리뷰 도서 목록 조회 (메인 페이지) """
    permission_classes = [AllowAny]

    def get(self, request):
        recent_reviews = Review.objects.select_related("book").order_by("-created_at")[:6]
        unique_books = list({review.book for review in recent_reviews})  # 중복 제거
        data = [{"title": book.title, "image_url": book.image_url} for book in unique_books]
        return Response(data, status=status.HTTP_200_OK)


class MyLibraryView(APIView):
    """ 내가 작성한 리뷰 목록 조회 (내 서재) """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_reviews = Review.objects.filter(user=request.user).select_related("book")
        books = list({review.book for review in user_reviews})  # 중복 제거된 도서 목록
        data = [
            {
                "title": book.title,
                "author": book.author,
                "image_url": book.image_url,
                "rating": round(
                    sum([r.rating for r in book.reviews.filter(user=request.user) if r.rating]) /
                    max(1, len([r.rating for r in book.reviews.filter(user=request.user) if r.rating])),
                    2
                ),
                "short_review": book.reviews.filter(user=request.user).first().content[:50] if book.reviews.filter(user=request.user).exists() else "",
            }
            for book in books
        ]
        return Response(data, status=status.HTTP_200_OK)


class BookReviewsView(APIView):
    """ 특정 책의 최신 리뷰 목록 조회 """
    permission_classes = [AllowAny]

    def get(self, request, book_id):
        reviews = Review.objects.filter(book__id=book_id).order_by("-created_at")
        data = [
            {
                "user": review.user.nickname,
                "rating": review.rating,
                "content": review.content[:50],  # 짧은 리뷰 내용만 표시
                "created_at": review.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for review in reviews
        ]
        return Response(data, status=status.HTTP_200_OK)