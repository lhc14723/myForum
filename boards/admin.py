from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Board, Post

admin.site.register(Board)
admin.site.register(Post)