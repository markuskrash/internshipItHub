
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class TaskStatus(models.TextChoices):
    """Статусы задачи"""
    ACTIVE = 'active', 'Активна'
    COMPLETED = 'completed', 'Завершена'


class Task(models.Model):
    """
    Поля:
        - id: Уникальный идентификатор
        - title: Название задачи
        - status: Состояние задачи (активна/завершена)
        - created_at: Дата и время создания
        - updated_at: Дата и время последнего обновления
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Название задачи',
        validators=[MinLengthValidator(1, message='Название не может быть пустым')]
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.ACTIVE,
        verbose_name='Состояние',
        help_text='Состояние задачи'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'{self.title} ({self.get_status_display()})'

    def is_active(self):
        """Проверка, активна ли задача"""
        return self.status == TaskStatus.ACTIVE

    def is_completed(self):
        """Проверка, завершена ли задача"""
        return self.status == TaskStatus.COMPLETED

