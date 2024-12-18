from django.db import models

class ModelConfiguration(models.Model):
    model = models.CharField(max_length=255, unique=True)  # 模型名称
    base_url = models.URLField(max_length=512)  # base_url