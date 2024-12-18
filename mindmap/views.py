from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MindMap
from .serializers import MindMapSerializer  # 需要为 MindMap 创建一个序列化器

class CreateMindMapView(APIView):
    def post(self, request, *args, **kwargs):
        # 确保当前用户关联到创建的思维导图
        serializer = MindMapSerializer(data=request.data)
        if serializer.is_valid():
            mind_map = serializer.save(user=request.user)  # 设置当前用户为思维导图的拥有者
            return Response(MindMapSerializer(mind_map).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SelectMindMapView(APIView):
    def get(self, request, *args, **kwargs):
        # 获取请求中的 title 参数（如果有的话）
        title = request.query_params.get('title')
        # 如果提供了 title 参数，则进行模糊查询
        if title:
            mind_maps = MindMap.objects.filter(user=request.user, is_del=False, title__icontains=title)
        else:
            # 如果没有提供 title 参数，则返回所有未删除的思维导图
            mind_maps = MindMap.objects.filter(user=request.user, is_del=False)
        # 序列化查询结果并返回
        serializer = MindMapSerializer(mind_maps, many=True)
        return Response(serializer.data)


class UpdateMindMapView(APIView):
    def put(self, request, *args, **kwargs):
        mind_map_id = kwargs.get('id')
        try:
            mind_map = MindMap.objects.get(id=mind_map_id, user=request.user)  # 只允许当前用户修改
        except MindMap.DoesNotExist:
            return Response({'error': 'Mind map not found or you do not have permission to edit'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MindMapSerializer(mind_map, data=request.data, partial=True)  # partial=True 表示只更新部分字段
        if serializer.is_valid():
            mind_map = serializer.save()  # 更新思维导图
            return Response(MindMapSerializer(mind_map).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteMindMapView(APIView):
    def delete(self, request, *args, **kwargs):
        mind_map_id = kwargs.get('id')
        try:
            mindmap = MindMap.objects.get(pk=mind_map_id, user=request.user)  # 只允许当前用户删除自己的思维导图
            mindmap.is_del = True
            mindmap.save()
            return Response({"message": "Mind map marked as deleted"}, status=status.HTTP_200_OK)
        except MindMap.DoesNotExist:
            return Response({"error": "Mind map not found or you do not have permission to delete"}, status=status.HTTP_404_NOT_FOUND)
