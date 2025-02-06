from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models.functions import TruncMonth
from django.db.models import Count
from datetime import datetime
from .models import Goal
from .serializers import GoalSerializer
from review.models import Review  # ✅ 리뷰 모델 가져오기

class GoalViewSet(ModelViewSet):
    """
    사용자별 목표 관리 (연간 목표만 유지)
    """
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoalProgressView(APIView):
    """
    목표 진행률 조회 API (읽은 책 개수 기준)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        goals = Goal.objects.filter(user=user)

        if not goals.exists():
            return Response({"error": "설정된 목표가 없습니다."}, status=404)

        progress_list = []
        for goal in goals:
            # ✅ 사용자가 리뷰를 남긴 유니크한 책 개수 계산 (중복 리뷰 제외)
            read_books_count = Review.objects.filter(user=user).values("book").distinct().count()

            # ✅ 진행률 계산 (목표 초과 허용)
            progress = (read_books_count / goal.total_books) * 100 if goal.total_books > 0 else 0

            progress_list.append({
                "goal_id": goal.id,
                "title": goal.title,
                "start_date": goal.start_date,
                "end_date": goal.end_date,
                "read_books": read_books_count,
                "goal_books": goal.total_books,
                "progress": f"{progress:.2f}%"
            })

        return Response(progress_list, status=200)

class MonthlyReadingProgressView(APIView):
    """
    월별 독서량 및 연간 목표 진행률 조회 API
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        current_year = datetime.now().year

        goal = Goal.objects.filter(user=user, start_date__year=current_year).first()
        if not goal:
            return Response({"error": "설정된 목표가 없습니다."}, status=404)

        monthly_reading = (
            Review.objects.filter(user=user, created_at__year=current_year)
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        monthly_data = {entry["month"].strftime("%Y-%m"): entry["count"] for entry in monthly_reading}

        total_read_books = sum(monthly_data.values())
        goal_books = goal.total_books
        progress = (total_read_books / goal_books) * 100 if goal_books > 0 else 0

        return Response({
            "goal": {
                "id": goal.id,
                "title": goal.title,
                "start_date": goal.start_date,
                "end_date": goal.end_date,
                "goal_books": goal_books,
                "read_books": total_read_books,
                "progress": f"{progress:.2f}%"
            },
            "monthly_reading": monthly_data
        }, status=200)
