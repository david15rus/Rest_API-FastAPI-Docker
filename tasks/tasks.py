import os

import pandas as pd
from celery import Celery
from dotenv import load_dotenv
from models import Dish, Menu, SubMenu
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = os.environ.get('DB_PORT')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_USER = os.environ.get('DB_USER')
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
RABBIT_MQ_URL = os.environ.get('RABBIT_MQ_URL')

celery_app = Celery(
    'tasks',
    broker=RABBIT_MQ_URL,
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

celery_app.conf.beat_schedule = {
    'sync-every-15-seconds': {
        'task': 'tasks.sync_excel_with_db',  # Путь к задаче
        'schedule': 15.0,  # Интервал в секундах
    },
}


@celery_app.task
def sync_excel_with_db():
    db = SessionLocal()
    path = os.path.join(os.path.dirname(__file__), '', 'admin', 'Menu.xlsx')
    df = pd.read_excel(path, header=None, engine='openpyxl')

    current_menu_id = None
    current_submenu_id = None

    for index, row in df.iterrows():
        if pd.notna(row[0]):
            menu_id, menu_title, menu_description, _, _, _ = row
            current_menu_id = menu_id

            exist_menu = db.query(Menu).filter(Menu.id == menu_id).first()
            if not exist_menu:
                new_menu = Menu(
                    id=menu_id,
                    title=menu_title,
                    description=menu_description
                )
                db.add(new_menu)
                db.commit()

        elif pd.notna(row[1]):
            _, submenu_id, submenu_title, submenu_description, _, _ = row
            current_submenu_id = submenu_id

            existing_submenu = db.query(SubMenu).filter(
                SubMenu.menu_id == current_menu_id, SubMenu.id == submenu_id).first()
            if not existing_submenu:
                new_submenu = SubMenu(
                    id=submenu_id,
                    title=submenu_title,
                    description=submenu_description,
                    menu_id=current_menu_id
                )
                db.add(new_submenu)
                db.commit()

        else:
            _, _, dish_id, dish_title, dish_description, price = row

            existing_dish = db.query(Dish).filter(Dish.id == dish_id, Dish.submenu_id == current_submenu_id).first()
            if not existing_dish:
                new_dish = Dish(
                    id=dish_id,
                    title=dish_title,
                    description=dish_description,
                    submenu_id=current_submenu_id,
                    price=float(price)
                )
                db.add(new_dish)
                db.commit()
