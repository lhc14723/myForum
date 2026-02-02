from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 创建路由器
router = DefaultRouter()
router.register(r'boards', views.BoardViewSet)  # 自动注册 boards/ 相关 URL
router.register(r'posts', views.PostViewSet)    # 自动注册 posts/ 相关 URL

urlpatterns = [
    # 包含路由器生成的 URL
    path('', include(router.urls)),
    
    # 认证相关 API
    path('auth/login/', views.api_login, name='api_login'),
    path('auth/logout/', views.api_logout, name='api_logout'),
    path('auth/register/', views.api_register, name='api_register'),
    
    # DRF 可浏览 API 登录页（浏览器里测试用）
    path('api-auth/', include('rest_framework.urls')),
]