from rest_framework import serializers
from .models import MindMap

class MindMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = MindMap
        fields = ['id', 'title', 'data', 'created_time', 'updated_time', 'is_del']

    def validate(self, attrs):
        if attrs['data'] == {}:
            attrs['data'] = {
                "data":{
                    "data": {
                        "text": attrs.get('title', '')  # 使用 title 设置 text 默认值
                    },
                    "children": []
                },
                "picUrl":""
            }
        return attrs

    def create(self, validated_data):
        # 使用 validate 方法中的默认数据来创建对象
        return super(MindMapSerializer, self).create(validated_data)