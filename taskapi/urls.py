
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Tasks API",
        default_version='v1',
        description="""
        REST API для управления задачами.
        
        ## Основные возможности:
        - Создание, чтение, обновление и удаление задач
        - Фильтрация и поиск задач
        - Пагинация результатов
        - Дополнительные действия (завершение, активация задач)
        
        ## Модель задачи:
        - **id**: Уникальный идентификатор (автоматически)
        - **title**: Назвние задачи (обязательное поле)
        - **status**: Состояние задачи (active/completed)
        - **created_at**: Дата и время создания
        - **updated_at**: Дата и время последнего обновления
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@tasks.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('tasks.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
