import os
from sqlalchemy.orm import declarative_base, relationship, backref, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship('Book', backref='publisher')

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    stocks = relationship('Stock', backref='shop')

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    publisher_id = Column(Integer, ForeignKey('publisher.id'))
    stocks = relationship('Stock', backref='book')

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'))
    shop_id = Column(Integer, ForeignKey('shop.id'))
    count = Column(Integer, nullable=False)


class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey('stock.id'))
    price = Column(Integer, nullable=False)
    date = Column(String, nullable=False)
    count = Column(Integer, nullable=False)


def create_tables(engine):
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    DSN = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(DSN)
    create_tables(engine)