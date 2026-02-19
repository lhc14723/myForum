from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Board, Post
from .serializers import BoardSerializer, PostSerializer, UserSerializer
from rest_framework.permissions import AllowAny 
from django.db.models.functions import Length


class BoardViewSet(viewsets.ModelViewSet):
    """
    分区 API
    list: GET /api/boards/          获取所有分区
    retrieve: GET /api/boards/1/    获取第1个分区详情
    create: POST /api/boards/       创建分区（需登录）
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # 任何人可读，登录可写


class PostViewSet(viewsets.ModelViewSet):
    """
    帖子 API
    支持：搜索、排序、分页
    """
    queryset = Post.objects.annotate(content_len=Length('content')).select_related('author', 'board')
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    
    # 配置过滤和搜索
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['board',]                    # 精确筛选：?board=1
    search_fields = ['title', 'content']            # 模糊搜索：?search=关键词
    ordering_fields = ['created_at', 'views', 'content_len']  # 排序：?ordering=content（短到长）或 -content（长到短）
    ordering = ['-created_at']                      # 默认排序
    
    def perform_create(self, serializer):
        """创建帖子时自动设置当前用户为作者"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'],permission_classes=[AllowAny])
    def increment_views(self, request, pk=None):
        """手动增加浏览量接口：POST /api/posts/1/increment_views/"""
        post = self.get_object()
        post.views += 1
        post.save()
        return Response({'status': 'views incremented', 'views': post.views})


# 用户认证相关 API（不使用模板）
@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    用户登录 API
    POST /api/login/
    Body: {"username": "xxx", "password": "xxx"}
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
            'message': '登录成功'
        })
    return Response({
        'success': False,
        'message': '用户名或密码错误'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    """登出 API：POST /api/logout/"""
    logout(request)
    return Response({'success': True, 'message': '已登出'})


@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    """
    注册 API
    POST /api/register/
    Body: {"username": "xxx", "password": "xxx", "email": "xxx@example.com"}
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if User.objects.filter(username=username).exists():
        return Response({
            'success': False,
            'message': '用户名已存在'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )
    return Response({
        'success': True,
        'user': UserSerializer(user).data,
        'message': '注册成功'
    }, status=status.HTTP_201_CREATED)