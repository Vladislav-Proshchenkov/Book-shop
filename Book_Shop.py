import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Book, Publisher, Shop, Stock, Sale

DSN = 'postgresql://postgres:23092011@localhost:5432/book_shop'
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

session.close()

if __name__ == '__main__':
    print('Список издателей:\n'
          '1. O’Reilly\n'
          '2. Pearson\n'
          '3. Microsoft Press\n'
          '4. No starch press\n')
    name_publisher = int(input('Введите номер издателя:'))
    if name_publisher < 1 or name_publisher > 4:
        print('Такого издателя нет')
        exit()

    for publisher in session.query(Publisher).filter(Publisher.id == name_publisher).all():
        for book in session.query(Book).filter(Book.id_publisher == name_publisher).all():
            a = book.title
            for sale in session.query(Sale).filter(Sale.id_stock == Stock.id, Stock.id_book == book.id).all():
                c = sale.price
                d = sale.date_sale
                e = book.id
                #print(a, e, c, d)
                for stock in session.query(Stock).filter(Stock.id == Sale.id_stock, Sale.id == sale.id).all():
                    # print(stock.id)
                    for shop in session.query(Shop).filter(Shop.id == Stock.id_shop, Stock.id == stock.id).all():
                        b = shop.name
                        print('Название книги:', a,'ID:', e,'Цена:', c, 'Дата:', d, 'Магазин:', b)