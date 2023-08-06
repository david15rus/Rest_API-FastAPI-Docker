# Используем базовый образ Python
FROM python:3.10-slim

# Установка зависимостей
WORKDIR /fastapi_app
COPY my_app/requirements.txt .
RUN apt-get update
RUN apt-get install -y libpq-dev gcc
RUN apt-get install -y postgresql
RUN apt-get install -y python3-psycopg2
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
COPY . .

# Запуск приложения
CMD ["uvicorn", "my_app.main_onion:app", "--host", "0.0.0.0", "--port", "8000"]
