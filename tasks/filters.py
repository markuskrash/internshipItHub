
import django_filters
from .models import Task, TaskStatus


class TaskFilter(django_filters.FilterSet):
    """Фильтр для задач"""
    
    status = django_filters.ChoiceFilter(
        choices=TaskStatus.choices,
        help_text='Фильтр по статусу задачи'
    )
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text='Поиск по названию (без учета регистра)'
    )
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        help_text='Задачи, созданные после указанной даты'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        help_text='Задачи, созданные до указанной даты'
    )

    class Meta:
        model = Task
        fields = ['status', 'title']

