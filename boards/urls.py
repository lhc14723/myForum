from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'boards', views.BoardViewSet)  
router.register(r'posts', views.PostViewSet)   

urlpatterns = [
    
    path('', include(router.urls)),
    
   
    path('auth/login/', views.api_login, name='api_login'),
    path('auth/logout/', views.api_logout, name='api_logout'),
    path('auth/register/', views.api_register, name='api_register'),
    
  
    path('api-auth/', include('rest_framework.urls')),
]
