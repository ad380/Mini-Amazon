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

    #this gets 100 products with the given offset for pagination
    @staticmethod
    def get_some(available=True, offset=0):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available, available_quantity
FROM Products
WHERE available = :available
LIMIT 100
OFFSET :offset
''',
                              available=available,
                              offset=offset)
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
    def get_by_price_asc(available=True, offset=0):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available, available_quantity
FROM Products
WHERE available = :available
ORDER BY price ASC
LIMIT 100
OFFSET :offset
''', 
                            available=available,
                            offset=offset)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_by_price_desc(available=True, offset=0):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available, available_quantity
FROM Products
WHERE available = :available
ORDER BY price DESC
LIMIT 100
OFFSET :offset
''', 
                            available=available,
                            offset=offset)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_by_category(category, offset=0):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available, available_quantity
FROM Products
WHERE category = :category
LIMIT 100
OFFSET :offset
''', 
                            category=category,
                            offset=offset)
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
RETURNING *
''',
                              id=id,
                              quantity=quantity)
            return rows
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
RETURNING *
''',
                              id=id)
            return rows
        except Exception:
            print("couldn't delete product")
            return None

# search for product given product name
    @staticmethod
    def search_products(searchValue):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available, available_quantity
FROM Products
WHERE lower(name) LIKE '%' || lower(:searchValue) || '%'
''', 
                            searchValue=searchValue)
        return [Product(*row) for row in rows]

