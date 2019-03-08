from django.contrib import admin
from .models import Board, Topic, Post


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_date', 'board', 'author')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'text', 'created_date',
        'picture', 'author'
    )
