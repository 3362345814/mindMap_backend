from django.urls import path
from .views import CreateMindMapView, SelectMindMapView, UpdateMindMapView, DeleteMindMapView

urlpatterns = [
    path('select/', SelectMindMapView.as_view(), name='list_mindmaps'),  # 获取所有思维导图
    path('create/', CreateMindMapView.as_view(), name='create_mindmap'),  # 创建思维导图
    path('update/<int:id>/', UpdateMindMapView.as_view(), name='update_mindmap'),  # 更新思维导图
    path('delete/<int:id>/', DeleteMindMapView.as_view(), name='delete_mindmap'),  # 删除思维导图
]
