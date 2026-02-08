# Generated migration for Task model

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Название задачи', max_length=200, validators=[django.core.validators.MinLengthValidator(1, message='Название не может быть пустым')], verbose_name='Название')),
                ('status', models.CharField(choices=[('active', 'Активна'), ('completed', 'Завершена')], default='active', help_text='Состояние задачи', max_length=20, verbose_name='Состояние')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['status'], name='tasks_task_status_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['-created_at'], name='tasks_task_created_idx'),
        ),
    ]

