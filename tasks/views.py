
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Task, TaskStatus
from .serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer
from .filters import TaskFilter
from .pagination import TaskPagination

logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    """
    Поддерживает стандартные операции CRUD:
    - GET /api/tasks/ - список всех задач
    - GET /api/tasks/{id}/ - получение задачи по ID
    - POST /api/tasks/ - создание новой задачи
    -PUT /api/tasks/{id}/ - полное обновление задачи
    - PATCH /api/tasks/{id}/ - частичное обновление задачи
    - DELETE /api/tasks/{id}/ - удаление задачи
    
    Дополнительные действия:
    - GET /api/tasks/active/ - список активных задач
    - GET /api/tasks/completed/ - список завершенных задач
    - POST /api/tasks/{id}/complete/ - завершить задачу
    - POST /api/tasks/{id}/activate/ - активировать задачу
    """
    queryset = Task.objects.all()
    permission_classes = [AllowAny]  # Для тестового задания разрешаем доступ всем
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title']
    ordering_fields = ['created_at', 'updated_at', 'title', 'status']
    ordering = ['-created_at']
    pagination_class = TaskPagination

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer

    def get_queryset(self):
        """Получние queryset с возможностью фильтрации"""
        queryset = super().get_queryset()
        
        # Дополнительная фильтрация по статусу через query параметры
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset

    def create(self, request, *args, **kwargs):
        """Создание новой задачи"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            task = serializer.save()
            logger.info(f'Создана новая задача: {task.id} - {task.title}')
            
            response_serializer = TaskSerializer(task)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f'Ошибка при создании задачи: {str(e)}')
            raise

    def update(self, request, *args, **kwargs):
        """Полное обновление задчи"""
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            task = serializer.save()
            logger.info(f'Обновлена задача: {task.id} - {task.title}')
            
            response_serializer = TaskSerializer(task)
            return Response(response_serializer.data)
        except Exception as e:
            logger.error(f'Ошибка при обновлении задачи: {str(e)}')
            raise

    def destroy(self, request, *args, **kwargs):
        """Удаление задачи"""
        try:
            instance = self.get_object()
            task_id = instance.id
            task_title = instance.title
            instance.delete()
            logger.info(f'Удалена задача: {task_id} - {task_title}')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f'Ошибка при удалении задачи: {str(e)}')
            raise

    @action(detail=False, methods=['get'], url_path='active')
    def active(self, request):
        """Получить список активных задач"""
        active_tasks = self.queryset.filter(status=TaskStatus.ACTIVE)
        page = self.paginate_queryset(active_tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(active_tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='completed')
    def completed(self, request):
        """Получить список завершенных задач"""
        completed_tasks = self.queryset.filter(status=TaskStatus.COMPLETED)
        page = self.paginate_queryset(completed_tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(completed_tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
        """Завершить задачу"""
        task = self.get_object()
        task.status = TaskStatus.COMPLETED
        task.save()
        logger.info(f'Задача {task.id} помечена как завершенная')
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='activate')
    def activate(self, request, pk=None):
        """Активировать задачу"""
        task = self.get_object()
        task.status = TaskStatus.ACTIVE
        task.save()
        logger.info(f'Задача {task.id} помечена как активная')
        serializer = self.get_serializer(task)
        return Response(serializer.data)

