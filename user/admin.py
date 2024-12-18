from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'api_key', 'model_configuration')  # 列表显示的字段
    search_fields = ('username', 'email')  # 添加搜索功能
