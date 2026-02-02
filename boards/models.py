

# Create your models here.

from django.db import models
from django.contrib.auth.models import User  # 使用 Django 内置用户模型
from django.db.models.functions import Length  # 用于按长度排序


class Board(models.Model):
    """论坛分区（如：技术讨论、闲聊、求职）"""
    name = models.CharField(max_length=100, unique=True, verbose_name='分区名称')
    description = models.TextField(verbose_name='分区描述')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'boards'
        verbose_name = '分区'
        verbose_name_plural = '分区'
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """帖子"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # 用户删除时，其帖子也删除
        related_name='posts',      # 可通过 user.posts 反向查询
        verbose_name='作者'
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,  # 分区删除时，帖子也删除
        related_name='posts',
        verbose_name='所属分区'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')  # 额外加的实用字段
    
    class Meta:
        db_table = 'posts'
        verbose_name = '帖子'
        verbose_name_plural = '帖子'
        ordering = ['-created_at']  # 默认按时间倒序
    
    def __str__(self):
        return self.title
    
    @property
    def content_length(self):
        """返回内容长度，用于排序"""
        return len(self.content)