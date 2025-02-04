from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer, NaverBookSerializer, BookWithReviewSerializer
from .models import Book
from review.models import Review
from .services import search_books_from_naver, get_book_by_isbn_from_naver

class SearchBookView(APIView):
    """
    네이버 API를 이용한 도서 검색 API
    """
    def get(self, request):
        query = request.GET.get("query", "")
        if not query:
            return Response({"error": "검색어를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

        data = search_books_from_naver(query)
        if data:
            serialized_data = NaverBookSerializer(data["items"], many=True).data
            return Response(serialized_data, status=status.HTTP_200_OK)
        return Response({"error": "네이버 API 호출 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetBookByISBNView(APIView):
    """
    ISBN을 이용한 개별 도서 조회 API
    """
    def get(self, request, isbn):
        data = get_book_by_isbn_from_naver(isbn)
        if data and data["items"]:
            serialized_data = NaverBookSerializer(data["items"][0]).data
            return Response(serialized_data, status=status.HTTP_200_OK)
        return Response({"error": "책을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

class RecentReviewView(APIView):
    """
    최근 리뷰된 도서 목록 조회 API
    """
    def get(self, request):
        recent_reviews = Review.objects.select_related("book").order_by("-created_at")[:10]  # 최신 리뷰 10개
        books = {review.book for review in recent_reviews}  # 중복 제거된 도서 목록
        serialized_books = BookWithReviewSerializer(books, many=True).data
        return Response(serialized_books, status=status.HTTP_200_OK)
