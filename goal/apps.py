from django.apps import AppConfig

class GoalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'goal'

    def ready(self):
        import goal.signals  # ✅ 시그널 자동 로드
