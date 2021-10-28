from flask import current_app as app


class Product:
    def __init__(self, id, seller_id, name, description, category, image,\
                 price, available, available_quantity):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.seller_id = seller_id

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available, available_quantity
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available, available_quantity
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all_by_seller(seller_id):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available, available_quantity
FROM Products
WHERE seller_id = :seller_id
''',
                              seller_id=seller_id)
        return [Product(*row) for row in rows]

