from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username
