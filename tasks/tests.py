
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task, TaskStatus


class TaskModelTest(TestCase):
    """Тесты модели Task"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.task = Task.objects.create(
            title='Тестовая задача',
            status=TaskStatus.ACTIVE
        )
    
    def test_task_creation(self):
        """Тест создания задачи"""
        self.assertEqual(self.task.title, 'Тестовая задача')
        self.assertEqual(self.task.status, TaskStatus.ACTIVE)
        self.assertTrue(self.task.is_active())
        self.assertFalse(self.task.is_completed())
    
    def test_task_str(self):
        """Тест строкового представления задачи"""
        expected = f'Тестовая задача ({self.task.get_status_display()})'
        self.assertEqual(str(self.task), expected)
    
    def test_task_completion(self):
        """Тест завершения задачи"""
        self.task.status = TaskStatus.COMPLETED
        self.task.save()
        self.assertTrue(self.task.is_completed())
        self.assertFalse(self.task.is_active())


class TaskAPITest(TestCase):

    def setUp(self):
        """Настройка тестовых данных"""
        self.client = APIClient()
        self.task = Task.objects.create(
            title='Тестовая задача',
            status=TaskStatus.ACTIVE
        )
    
    def test_create_task(self):
        """Тест создания задачи через API"""
        url = reverse('task-list')
        data = {
            'title': 'Новая задача',
            'status': TaskStatus.ACTIVE
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(response.data['title'], 'Новая задача')
    
    def test_get_task_list(self):
        """Тест получения списка задач"""
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_task_detail(self):
        """Тест получения задачи по ID"""
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.task.pk)
        self.assertEqual(response.data['title'], self.task.title)
    
    def test_update_task(self):
        """Тест обновления задачи"""
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        data = {
            'title': 'Обновленная задача',
            'status': TaskStatus.COMPLETED
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Обновленная задача')
        self.assertEqual(self.task.status, TaskStatus.COMPLETED)
    
    def test_partial_update_task(self):
        """Тест частичного обновления задачи"""
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        data = {'status': TaskStatus.COMPLETED}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, TaskStatus.COMPLETED)
    
    def test_delete_task(self):
        """Тест удаления задачи"""
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
    
    def test_get_active_tasks(self):
        """Тест получения активных задач"""
        Task.objects.create(title='Завершенная задача', status=TaskStatus.COMPLETED)
        url = reverse('task-active')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], TaskStatus.ACTIVE)
    
    def test_get_completed_tasks(self):
        """Тест получения завершенных задач"""
        Task.objects.create(title='Завершенная задача', status=TaskStatus.COMPLETED)
        url = reverse('task-completed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], TaskStatus.COMPLETED)
    
    def test_complete_task(self):
        """Тест завершения задачи через действие"""
        url = reverse('task-complete', kwargs={'pk': self.task.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, TaskStatus.COMPLETED)
    
    def test_activate_task(self):
        """Тест активации задачи через действие"""
        self.task.status = TaskStatus.COMPLETED
        self.task.save()
        url = reverse('task-activate', kwargs={'pk': self.task.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, TaskStatus.ACTIVE)
    
    def test_validation_empty_title(self):
        """Тест валидации пустого названия"""
        url = reverse('task-list')
        data = {'title': '', 'status': TaskStatus.ACTIVE}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_filter_by_status(self):
        """Тест фильтрации по статусу"""
        Task.objects.create(title='Завершенная задача', status=TaskStatus.COMPLETED)
        url = reverse('task-list')
        response = self.client.get(url, {'status': TaskStatus.COMPLETED})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], TaskStatus.COMPLETED)
    
    def test_search_by_title(self):
        """Тест поиска по названию"""
        Task.objects.create(title='Другая задача', status=TaskStatus.ACTIVE)
        url = reverse('task-list')
        response = self.client.get(url, {'search': 'Тестовая'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Тестовая задача')

