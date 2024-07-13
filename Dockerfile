FROM python:3.12

# Установите рабочую директорию в контейнере
WORKDIR /app

RUN ln -sf /usr/share/zoneinfo/Asia/Almaty /etc/localtime && echo "Asia/Almaty" > /etc/timezone

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
RUN python manage.py collectstatic --no-input
COPY backup.sh /app/backup.sh
