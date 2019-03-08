from django.contrib import admin
from .models import DrawingModel



@admin.register(DrawingModel)
class DrawingModelAdmin(admin.ModelAdmin):
    list_display = ('title',)

