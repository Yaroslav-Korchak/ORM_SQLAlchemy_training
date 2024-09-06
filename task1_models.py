from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), nullable=True)
    books = relationship('Book', backref='book')


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(length=255), nullable=True)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=True)
    stocks = relationship('Stock', backref='book')

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), nullable=True)


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=True)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=True)
    count = Column(Integer, default=0, nullable=True)


class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Float, default=None)
    date_sale = Column(DateTime, default=None)
    id_stock = Column(Integer, ForeignKey('stock.id'))
    count = Column(Integer, default=0, nullable=True)
    stock = relationship(Stock, backref='sales')
