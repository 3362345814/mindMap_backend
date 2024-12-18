from django.contrib.auth.models import AbstractUser
from django.db import models

from ai.models import ModelConfiguration


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # 设置 email 字段唯一
    api_key = models.CharField(max_length=255, blank=True, null=True, verbose_name="API Key")  # 大模型 API Key
    model_configuration = models.ForeignKey(
        ModelConfiguration,  # 外键关联到 ModelConfiguration 表
        on_delete=models.SET_NULL,  # 如果删除 ModelConfiguration，设置为 NULL
        null=True,  # 允许为空
        blank=True,  # 允许为空
        verbose_name="Model Configuration"  # 字段名称
    )
    # 自定义模型名称
    custom_model = models.CharField(max_length=255, blank=True, null=True, verbose_name="Custom Model Name")
    # 自定义 base_url
    custom_base_url = models.URLField(max_length=512, blank=True, null=True, verbose_name="Custom Base URL")

    # 模型选择状态
    MODEL_CHOICES = [
        ('custom', 'Custom Model'),
        ('default', 'Default Model'),
        ('select', 'Select')
    ]
    model_selection_status = models.CharField(
        max_length=10,
        choices=MODEL_CHOICES,
        default='default',
        verbose_name="Model Selection Status"
    )