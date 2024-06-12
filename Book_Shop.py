import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Book, Publisher, Shop, Stock, Sale

DSN = 'postgresql://postgres:postgres@localhost:5432/book_shop'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

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

def get_shops():
    books = session.query(Book, Publisher, Stock, Shop, Sale).select_from(Book).join(Publisher).join(Stock).join(Shop).join(Sale)
    return books

def get_name(publisher_name):
    if publisher_name.isdigit():
        publisher_name = int(publisher_name)
        for book, publisher, stock, shop, sale in get_shops():
            if publisher.id == publisher_name:
                print('Название книги:', book.title, 'Цена:', sale.price, 'Дата:', sale.date_sale, 'Магазин:', shop.name)
    else:
        for book, publisher, stock, shop, sale in get_shops():
            if publisher.name == publisher_name:
                print('Название книги:', book.title, 'Цена:', sale.price, 'Дата:', sale.date_sale, 'Магазин:', shop.name)

session.close()

if __name__ == '__main__':
    print('Список издателей:\n'
          '1. O’Reilly\n'
          '2. Pearson\n'
          '3. Microsoft Press\n'
          '4. No starch press\n')
    get_name(publisher_name = input('Введите имя издателя:'))
    get_shops()