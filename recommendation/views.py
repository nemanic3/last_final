from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Recommendation
from .serializers import RecommendationSerializer
from .services import get_book_recommendations

class RecommendationViewSet(ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def get_queryset(self):
        # 인증되지 않은 사용자는 빈 queryset 반환
        if self.request.user.is_anonymous:
            return Recommendation.objects.none()
        # 인증된 사용자는 자신의 추천 데이터만 반환
        return self.queryset.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        네이버 API를 활용한 추천 도서 리스트 반환
        """
        query = request.GET.get("query", "")
        if not query:
            return Response({"error": "검색어를 입력하세요."}, status=400)

        recommended_books = get_book_recommendations(query)
        return Response(recommended_books, status=200)
