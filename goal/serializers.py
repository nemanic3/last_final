from rest_framework import serializers
from .models import Goal
from review.models import Review  # ✅ 리뷰 모델 가져오기

class GoalSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()  # ✅ 진행률 계산 필드 추가

    class Meta:
        model = Goal
        fields = '__all__'

    def validate(self, data):
        """ 시작 날짜가 종료 날짜보다 늦으면 안됨 """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({"error": "시작 날짜는 종료 날짜보다 이전이어야 합니다."})
        return data

    def get_progress(self, obj):
        """ 목표 진행률 계산 (읽은 책 개수 기준) """
        # ✅ 사용자가 리뷰를 남긴 유니크한 책 개수 계산 (중복 리뷰 제외)
        unique_read_books = Review.objects.filter(user=obj.user).values("book").distinct().count()

        # ✅ 진행률 계산 (목표 초과 허용)
        progress = (unique_read_books / obj.total_books) * 100 if obj.total_books > 0 else 0
        return round(progress, 2)  # ✅ 소수점 2자리까지 표시
