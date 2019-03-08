from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    # authorはForeignKeyで設定している。
    list_display = ('a_title', 'created_date', 'author', )
    list_filter = ['created_date']
    search_fields = ['a_title', 'text']


admin.site.register(Article, ArticleAdmin)
