from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class MindMap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    data = models.JSONField()  # 存储思维导图的完整 JSON 数据
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_del = models.BooleanField(default=False)


    def __str__(self):
        return self.title
