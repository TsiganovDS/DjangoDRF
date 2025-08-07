# Указываем базовый образ
FROM python:3.13.3

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Создать виртуальное окружение
RUN python3 -m venv /opt/venv

# Активировать виртуальное окружение (внутри RUN-конструкции)
ENV PATH="/opt/venv/bin:$PATH"

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .



RUN mkdir -p /lms/media


# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]