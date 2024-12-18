from rest_framework import serializers
from .models import ModelConfiguration

class ModelConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelConfiguration
        fields = ['id', 'model', 'base_url']