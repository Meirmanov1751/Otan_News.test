from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Установить модуль настроек Django для celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Otan_news.settings')

app = Celery('Otan_news')

# Использовать настройки из settings.py с префиксом CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически загружать задачи из приложений
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')