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
`python -m venv venv`
`source venv/bin/activate`
Для Windows используйте `venv\Scripts\activate`
3. Склонируйте репозиторий:
`git clone https://github.com/david15rus/Rest_API-FastAPI-Docker.git`
4. Установите зависимости:
`pip install -r .\my_app\requirements.txt`
5. Создать файл .env со следующей структурой:
    - DB_HOST='postgres_restaurant'
    - DB_PORT='5432'
    - DB_NAME='Fast_API'
    - DB_USER='postgres'
    - DB_PASSWORD='postgres'
    - POSTGRES_USER='postgres'
    - POSTGRES_PASSWORD='postgres'
    - PGUSER='postgres'
    - DATABASE_URL='postgresql+asyncpg://postgres:postgres@postgres_restaurant/Fast_API'
    - REDIS_URI='redis://redis_app:6379'
6. В файле docker-compose.yaml изменить строчку 80:
    `volumes:`
      `- D:\Job\Python_projects\FastAPI(Docker)\admin:/celery-app/admin`
на
    `volumes:`
      `- <Путь до папки admin>\admin:/celery-app/admin`
6. Cоздать образ docker-compose командой
`docker compose build`
7. Создать контейнеры, на основе собранного образа, командой
`docker copmose up -d`
## Запуск
Теперь API запущен и доступ к нему можно получить по адресу http://localhost:8000.
Но для запуска тестов потребуется ввести еще одну команду:
`docker exec -it fastapi_restaurant pytest tests/`


## Задания со звездочкой
1) Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос.
Реализация находится в my_app/repositories/menu_repositories.py функция get_dish_and_submenus_count
строка 74
2) Описать ручки API в соответствии с OpenAPI
Реализация - все файлы в папке my_app/endpoints. В данном случае имеется в виду документация для каждого
эндпоинта, и отображение примера ответа в swagger (http://localhost/docs)
3) Реализовать в тестах аналог Django reverse() для FastAPI
Реализовал, используя router и их имена. Соответственно уже из тестов обращался к ручкам не по полному пути,
а получал путь до эндпоинтов используя функцию URLPath(app.url_path_for(endpoint_name, CGI_params))
Реализация в коде в папке my_app/endpoints во всех эндпоинтах и использовал в коде в папке
my_app/tests
