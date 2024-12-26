from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model

from ai.models import ModelConfiguration

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        email = data.get('email')
        code = data.get('code')
        try:
            validate_password(password)  # 这里调用所有配置的密码验证器
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        password = data.get('password')
        try:
            validate_password(password)  # 调用 Django 密码验证器
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})
        return data


# 修改用户名序列化器
class UpdateUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)

    def validate(self, value):
        if User.objects.filter(username=value['username']).exists():
            raise serializers.ValidationError("用户名已存在。")
        return value

# 修改 api_key 和 base_url 序列化器
class UpdateAPIKeyAndBaseURLSerializer(serializers.Serializer):
    api_key = serializers.CharField(max_length=255, required=True)
    model_configuration_id = serializers.IntegerField(required=True)
    custom_model = serializers.CharField(max_length=255, required=False, allow_blank=True)
    custom_base_url = serializers.URLField(max_length=512, required=False, allow_blank=True)
    model_selection_status = serializers.ChoiceField(
        choices=['custom', 'default', 'none'], required=False, default='none'
    )
