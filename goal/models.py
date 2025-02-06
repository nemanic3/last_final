import datetime
from django.db import models
from django.conf import settings

class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField()
    total_books = models.IntegerField(default=0)  # ✅ 목표 책 수
    read_books = models.IntegerField(default=0)  # ✅ 현재까지 읽은 책 개수
    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'goal'

    def __str__(self):
        return f"{self.user.nickname} - {self.title}"
