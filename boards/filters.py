from django_filters import rest_framework as filters
from .models import Post


class PostFilter(filters.FilterSet):
    
    
    author_username = filters.CharFilter(
        field_name='author__username',
        lookup_expr='icontains'
    )
    
    class Meta:
        model = Post
        fields = ['board', 'author']
