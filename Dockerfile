# Указываем базовый образ
FROM python:3.13.3

# Устанавливаем рабочую директорию в контейнере
WORKDIR /lms

RUN apt-get update  \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .

ENV SECRET_KEY=SECRET_KEY
ENV CELERY_BROKER_URL='redis://redis:6379/0'
ENV CELERY_BACKEND='redis://redis:6379/0'

RUN mkdir -p /lms/media

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]