# Use a base image that supports both Django and FastAPI
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Set timezone
RUN ln -sf /usr/share/zoneinfo/Asia/Almaty /etc/localtime && echo "Asia/Almaty" > /etc/timezone

# Install necessary system packages
RUN apt-get update \
    && apt-get install -y build-essential gcc python3-dev \
    && apt-get clean

# Copy requirements.txt and install dependencies
COPY . /app
RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

# Copy the rest of the application code


# Collect static files for Django
RUN python manage.py collectstatic --no-input

# Expose ports for Django and FastAPI
EXPOSE 8000
EXPOSE 8001

# Command to run Gunicorn for Django and Uvicorn for FastAPI
CMD ["sh", "-c", "gunicorn Otan_news.wsgi:application --bind 0.0.0.0:8000 & uvicorn admin_api.main:app --host 0.0.0.0 --port 8001"]
