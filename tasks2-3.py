from task1_models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import json


load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DSN = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

def create_tables():
    with open('fixtures/test_data.json', 'r') as fd:
        data = json.load(fd)

    # Загрузка данных в базу
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]

        session.add(model(id=record.get('pk'), **record.get('fields')))

    session.commit()
    print("Данные успешно загружены!")

def fetch_books_by_publisher(publisher_identifier):
    if isinstance(publisher_identifier, str):
        # Если входное значение — это строка, считаем, что это название издателя
        filter_condition = Publisher.name == publisher_identifier
    elif isinstance(publisher_identifier, int):
        # Если входное значение — это целое число, считаем, что это ID издателя
        filter_condition = Publisher.id == publisher_identifier
    else:
        raise ValueError("Идентификатором издателя может быть строка(Название издателя) или число(ID издателя)")

    results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        join(Stock, Stock.id_book == Book.id).\
        join(Shop, Shop.id == Stock.id_shop).\
        join(Sale, Sale.id_stock == Stock.id).\
        join(Publisher, Publisher.id == Book.id_publisher).\
        filter(filter_condition).\
        all()

    if not results:
        print(f"По запросу '{publisher_identifier}' ничего не найдено.")
        return

    for result in results:
        book_title, shop_name, price, date = result
        print(f"{book_title} | {shop_name} | {price} | {date}")

# Примеры использования:
# fetch_books_by_publisher('Publisher Name')  # Поиск по названию
# fetch_books_by_publisher(1)  # Поиск по ID


def clear_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

clear_tables(engine)
create_tables()
publisher_name = input('Введите название издателя: ')
fetch_books_by_publisher(publisher_name)
