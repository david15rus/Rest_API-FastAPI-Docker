# FastAPI_project

Данный API предлагается в дух видах: синхронном и асинхронном.
API позволяет совершать CRUD операции посредством использования ORM SQLAlchemy 
и СУБД PostgresSQL

## Требования
Для правильного функционирования API необходимо, что бы 
все версии библиотек и модулей соотвествовали файлу requirements.txt.
А также версии Python и Postgres:
- Python 3.10 (или новее)
- PostgreSQL 15 (или новее)

## Установка
1. Создайте виртуальное окружение и активируйте его:
python -m venv venv
2. Склонируйте репозиторий:
git clone https://github.com/david15rus/Rest_API-FastAPI-Docker-.git
source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
3. Установите зависимости:
pip install -r .\myapp\requirements.txt
4. Создать файл .env со следующей структурой:
    - DB_HOST='postgres_restaurant'
    - DB_PORT='5432'
    - DB_NAME='Fast_API'
    - DB_USER='postgres'
    - DB_PASSWORD='postgres'
    - POSTGRES_USER='postgres'
    - POSTGRES_PASSWORD='postgres'
    - PGUSER='postgres'
    - DATABASE_URL='postgresql+asyncpg://postgres:postgres@postgres_restaurant/Fast_API'
5. Cоздать образ docker-compose командой 
docker compose build
6. Создать контейнеры, на основе собранного образа, командой 
docker copmose up -d   
## Запуск
Теперь API запущен и доступ к нему можно получить по адресу http://localhost:8000. 
Но для запуска тестов потребуется ввести еще одну команду:
docker exec -it fastapi_restaurant /bin/sh 
