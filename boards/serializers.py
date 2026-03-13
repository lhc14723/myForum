from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Board, Post


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']


class BoardSerializer(serializers.ModelSerializer):
    """分区序列化器"""
    post_count = serializers.IntegerField(source='posts.count', read_only=True)
    
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'created_at', 'post_count']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    board_name = serializers.CharField(source='board.name', read_only=True)
    
   
    content_length = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'content_length', 
            'author',
            'board', 'board_name',
            'created_at', 'updated_at', 'views'
        ]
        read_only_fields = ['views', 'created_at', 'updated_at']
    
  
    def get_content_length(self, obj):
        return len(obj.content)
