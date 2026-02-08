
from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Административная панель для задач"""
    
    list_display = ['id', 'title', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['title']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_editable = ['status']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('id', 'title', 'status')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

