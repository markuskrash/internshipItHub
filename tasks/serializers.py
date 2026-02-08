
from rest_framework import serializers
from .models import Task, TaskStatus


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Task"""
    
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True,
        help_text='Отображаемое название статуса'
    )
    is_active = serializers.BooleanField(read_only=True, help_text='Активна ли задача')
    is_completed = serializers.BooleanField(read_only=True, help_text='Завершена ли задача')

    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'status_display', 'is_active', 
                  'is_completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'title': {
                'help_text': 'Название задачи (обязательное поле)',
                'required': True,
                'allow_blank': False,
            },
            'status': {
                'help_text': 'Состояние задачи: active (активна) или completed (завершена)',
                'required': False,
            }
        }

    def validate_title(self, value):
        """Валидация названия задачи"""
        if not value or not value.strip():
            raise serializers.ValidationError('Название задачи не может быть пустым')
        if len(value.strip()) < 1:
            raise serializers.ValidationError('Название задачи должно содержать хотя бы один символ')
        return value.strip()

    def validate_status(self, value):
        """Валидация статуса задачи"""
        valid_statuses = [choice[0] for choice in TaskStatus.choices]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f'Недопустимый статус. Допустимые значения: {", ".join(valid_statuses)}'
            )
        return value


class TaskCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания задачи (упрощенный)"""
    
    class Meta:
        model = Task
        fields = ['title', 'status']
        extra_kwargs = {
            'title': {'required': True},
            'status': {'required': False, 'default': TaskStatus.ACTIVE}
        }

    def validate_title(self, value):
        """Валидация названия задачи"""
        if not value or not value.strip():
            raise serializers.ValidationError('Название задачи не может быть пустым')
        return value.strip()


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления задачи"""
    
    class Meta:
        model = Task
        fields = ['title', 'status']
        extra_kwargs = {
            'title': {'required': False},
            'status': {'required': False}
        }

    def validate_title(self, value):
        """Валидация названия задачи"""
        if value is not None:
            if not value.strip():
                raise serializers.ValidationError('Название задачи не может быть пустым')
            return value.strip()
        return value

