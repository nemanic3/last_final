import datetime
from django.db import models
from django.conf import settings

class Goal(models.Model):
    GOAL_TYPE_CHOICES = [
        ('annual', '연간 목표'),
        ('monthly', '월간 목표'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    goal_type = models.CharField(max_length=10, choices=GOAL_TYPE_CHOICES, default='annual')
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'goal'

    def __str__(self):
        return f"{self.user.nickname} - {self.title}"
