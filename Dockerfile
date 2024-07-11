#FROM python:3.12
#
#WORKDIR /app
#
## Установите необходимые библиотеки
#RUN apt-get update \
#    && apt-get install -y build-essential gcc python3-dev \
#    && apt-get clean
#
## Установите зависимости из requirements.txt
#COPY requirements.txt .
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
#
## Копируйте содержимое текущей папки в рабочую директорию контейнера
#COPY . .
#
## Выполните миграции базы данных
#RUN python manage.py makemigrations
#RUN python manage.py migrate
#
#
## Откройте порт для приложения
#EXPOSE 8000
#
## Укажите команду по умолчанию для запуска приложения
#CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
# syntax=docker/dockerfile:1
FROM python:3.12

# Установите рабочую директорию в контейнере
WORKDIR /app

RUN apt-get update \
    && apt-get install -y build-essential gcc python3-dev \
    && apt-get clean
# Скопируйте файлы требований
COPY requirements.txt /app
RUN pip install --upgrade pip

# Установите зависимости
RUN pip install -r requirements.txt

# Скопируйте остальные файлы проекта
COPY . /app
RUN python manage.py collectstatic
COPY backup.sh /app/backup.sh
#RUN chmod +x /usr/src/app/backup.sh
#RUN echo "0 0 * * * /bin/bash /usr/src/app/backup.sh >> /usr/src/app/backup.log 2>&1" > /etc/cron.d/backup-cron
#RUN crontab /etc/cron.d/backup-cron
#CMD ["cron", "-f"]