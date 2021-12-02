from flask import current_app as app


class Product:
    def __init__(self, id, seller_id, name, description, category, image,\
                 price, available, available_quantity):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.seller_id = seller_id
        self.description = description
        self.category = category
        self.image = image
        self.available_quantity = available_quantity

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

    @staticmethod
    def get_sellers():
        rows = app.db.execute('''
SELECT seller_id
FROM Products
'''
                              )
        return [row[0] for row in rows]


    @staticmethod
    def get_by_price_asc(available=True):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available, available_quantity
FROM Products
WHERE available = :available
ORDER BY price ASC
''', 
                            available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_by_price_desc(available=True):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available, available_quantity
FROM Products
WHERE available = :available
ORDER BY price DESC
''', 
                            available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_by_category(category):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available, available_quantity
FROM Products
WHERE category = :category
''', 
                            category=category)
        return [Product(*row) for row in rows]


    @staticmethod
    def get_names(pid):
        #pids is list of pids
        rows = app.db.execute('''
    SELECT name
    FROM Products
    WHERE id = :pid
    ''', 
                            pid=pid)
        return rows[0][0]


#add new product
    @staticmethod
    def addProduct(seller_id, name, description, category, price, available_quantity):
        try:
            rows = app.db.execute("""
INSERT INTO Products(seller_id, name, description, category, image,
price, available, available_quantity)
VALUES(:seller_id, :name, :description, :category, 'url', :price, True, :available_quantity)
RETURNING id
""",
                                  seller_id = seller_id,
                                  name = name,
                                  description = description,
                                  category = category,
                                  price=price,
                                  available_quantity=available_quantity)
            id = rows[0][0]
            return Product.get(id)
        except Exception:
            print("Couldn't add product")
            return None

# update purchase status for given product id
    @staticmethod
    def editQuantity(id, quantity):
        try:
            rows = app.db.execute('''
UPDATE Products
SET available_quantity = :quantity
WHERE id = :id
''',
                              id=id,
                              quantity=quantity)
            return id
        except Exception:
            print("couldn't update product quantity")
            return None

# delete product with given product id
    @staticmethod
    def deleteProduct(id):
        try:
            rows = app.db.execute('''
DELETE FROM Products
WHERE id = :id
''',
                              id=id)
            return id
        except Exception:
            print("couldn't delete product")
            return None

