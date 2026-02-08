# Tasks REST API

Профессиональный REST API для управления задачами, реализованный на Django и Django REST Framework.

## Возможности

- Полный CRUD функционал для задач
- Поиск и фильтрация задач
- Пагинация результатов
- Автоматическая документация API (Swagger/OpenAPI)
- Валидация данных
- Покрытие тестами
- Логирование операций
- Дополнительные действия (завершение/активация задач)

## Требования

- Python 3.10+
- Django 6.0+
- Django REST Framework 3.15+

## Установка

1. **Клонируйте репозиторий или перейдите в директорию проекта:**

```bash
cd taskapi-project
```

2. **Создайте виртуальное окружение:**

```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/Mac
# или
venv\Scripts\activate  # Для Windows
```

3. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

4. **Создайте файл `.env` на основе `.env.example`:**

```bash
cp .env.example .env
```

5. **Примените миграции:**

```bash
python manage.py migrate
```

6. **Создайте суперпользователя (опционально):**

```bash
python manage.py createsuperuser
```

7. **Запустите сервер разработки:**

```bash
python manage.py runserver
```

API будет доступен по адресу: `http://127.0.0.1:8000/`

## Документация API

После запуска сервера документация доступна по следующим адресам:

- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/
- **API Docs**: http://127.0.0.1:8000/api/docs/
- **JSON Schema**: http://127.0.0.1:8000/swagger.json
- **YAML Schema**: http://127.0.0.1:8000/swagger.yaml

## API Endpoints

### Базовый URL: `/api/`

#### Задачи (Tasks)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/tasks/` | Получить список всех задач |
| POST | `/api/tasks/` | Создать новую задачу |
| GET | `/api/tasks/{id}/` | Получить задачу по ID |
| PUT | `/api/tasks/{id}/` | Полное обновление задачи |
| PATCH | `/api/tasks/{id}/` | Частичное обновление задачи |
| DELETE | `/api/tasks/{id}/` | Удалить задачу |
| GET | `/api/tasks/active/` | Получить список активных задач |
| GET | `/api/tasks/completed/` | Получить список завершенных задач |
| POST | `/api/tasks/{id}/complete/` | Завершить задачу |
| POST | `/api/tasks/{id}/activate/` | Активировать задачу |

### Параметры запросов

#### Фильтрация и поиск

- `status` - фильтр по статусу (`active` или `completed`)
- `title` - поиск по названию (без учета регистра)
- `search` - общий поиск по названию
- `created_after` - задачи, созданные после указанной даты (формат: `YYYY-MM-DDTHH:MM:SS`)
- `created_before` - задачи, созданные до указанной даты

#### Сортировка

- `ordering` - сортировка по полям: `created_at`, `updated_at`, `title`, `status`
- Пример: `?ordering=-created_at` (сортировка по дате создания, по убыванию)

#### Пагинация

- `page` - номер страницы
- `page_size` - количество элементов на странице (максимум 100)

## Примеры использования

### Создание задачи

```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Новая задача",
    "status": "active"
  }'
```

### Получение списка задач

```bash
curl http://127.0.0.1:8000/api/tasks/
```

### Получение задачи по ID

```bash
curl http://127.0.0.1:8000/api/tasks/1/
```

### Обновление задачи

```bash
curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

### Фильтрация по статусу

```bash
curl http://127.0.0.1:8000/api/tasks/?status=active
```

### Поиск по названию

```bash
curl http://127.0.0.1:8000/api/tasks/?search=важное
```

### Завершение задачи

```bash
curl -X POST http://127.0.0.1:8000/api/tasks/1/complete/
```

## Модель данных

### Task (Задача)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный идентификатор (автоматически) |
| `title` | String | Название задачи (обязательное, 1-200 символов) |
| `status` | String | Состояние: `active` (активна) или `completed` (завершена) |
| `created_at` | DateTime | Дата и время создания (автоматически) |
| `updated_at` | DateTime | Дата и время последнего обновления (автоматически) |

## Тестирование

Запуск тестов:

```bash
python manage.py test
```

Или с покрытием:

```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Структура проекта

```
taskapi-project/
├── taskapi/                 # Основные настройки проекта
│   ├── settings.py          # Настройки Django
│   ├── urls.py              # Главный URL конфиг
│   ├── wsgi.py              # WSGI конфигурация
│   └── asgi.py              # ASGI конфигурация
├── tasks/                   # Приложение для задач
│   ├── models.py           # Модель Task
│   ├── serializers.py      # Сериализаторы
│   ├── views.py            # ViewSets
│   ├── filters.py          # Фильтры
│   ├── pagination.py       # Настройки пагинации
│   ├── urls.py             # URL маршруты API
│   ├── admin.py            # Админ-панель
│   ├── tests.py            # Тесты
│   └── migrations/         # Миграции БД
├── manage.py               # Утилита управления Django
├── requirements.txt        # Зависимости проекта
├── README.md               # Документация
└── .env.example            # Пример конфигурации
```

## Конфигурация

Настройки проекта можно изменить через переменные окружения в файле `.env`:

- `SECRET_KEY` - секретный ключ Django
- `DEBUG` - режим отладки (True/False)
- `ALLOWED_HOSTS` - разрешенные хосты (через запятую)
- `DJANGO_LOG_LEVEL` - уровень логирования

## Деплой

Для продакшена рекомендуется:

1. Установить `DEBUG=False` в `.env`
2. Настроить `ALLOWED_HOSTS`
3. Использовать PostgreSQL вместо SQLite
4. Настроить статические файлы (WhiteNoise)
5. Использовать Gunicorn или uWSGI
6. Настроить Nginx как reverse proxy

## Особенности реализации

- Использование Django REST Framework для профессионального API
- ViewSets для стандартизированных CRUD операций
- Сериализаторы с валидацией данных
- Фильтрация через django-filter
- Пагинация результатов
- Автоматическая документация через drf-yasg
- Логирование всех операций
- Индексы в базе данных для оптимизации
- Полное покрытие тестами
- Обработка ошибок
- Поддержка переменных окружения


