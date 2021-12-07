from flask import current_app as app


class Product:
    def __init__(self, id, seller_id, name, description, category, image,\
                 price, available_quantity):
        self.id = id
        self.name = name
        self.price = price
        self.seller_id = seller_id
        self.description = description
        self.category = category
        self.image = image
        self.available_quantity = available_quantity

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available_quantity
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available_quantity
FROM Products
WHERE available_quantity > 0
''',
                              )
        return [Product(*row) for row in rows]

    #this gets 100 products with the given offset for pagination
    @staticmethod
    def get_some(offset=0):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available_quantity
FROM Products
WHERE available_quantity > 0
ORDER BY id
LIMIT 50
OFFSET :offset
''',
                              offset=offset
        )
        return [Product(*row) for row in rows]

    #this takes a list of product id's and gets those products
    @staticmethod
    def get_these_products(pids, offset=0):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available_quantity
FROM Products
WHERE id = :pids
AND available_quantity > 0
LIMIT 50
OFFSET :offset
        ''',
                            offset=offset)

#this gets only products sold by a specific seller
    @staticmethod
    def get_all_by_seller(seller_id):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available_quantity
FROM Products
WHERE seller_id = :seller_id
''',
                              seller_id=seller_id)
        return [Product(*row) for row in rows]

#this is a list of sellers
    @staticmethod
    def get_sellers():
        rows = app.db.execute('''
SELECT seller_id
FROM Products
'''
                              )
        return [row[0] for row in rows]

#this sorts the products by ascending order
    @staticmethod
    def get_by_price_asc(offset=0):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available_quantity
FROM Products
WHERE available_quantity > 0
ORDER BY price ASC
LIMIT 50
OFFSET :offset
''', 
                            
                            offset=offset)
        return [Product(*row) for row in rows]

#this sorts the products by descending order
    @staticmethod
    def get_by_price_desc(offset=0):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available_quantity
FROM Products
WHERE available_quantity > 0
ORDER BY price DESC
LIMIT 50
OFFSET :offset
''', 
                            
                            offset=offset)
        return [Product(*row) for row in rows]

#this sorts the products by average rating from highest to lowest
    @staticmethod
    def get_by_rating(offset=0):
        rows = app.db.execute('''
SELECT AVG(r.rating), r.product_id
FROM ProductReviews r, Products p
WHERE r.product_id = p.id 
GROUP BY r.product_id
ORDER BY AVG(r.rating) DESC
LIMIT 50
OFFSET :offset
        ''',
                            offset=offset)
        return [row[1] for row in rows]

#this filters products by category
    @staticmethod
    def get_by_category(category, offset=0):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available_quantity
FROM Products
WHERE category = :category
LIMIT 50
OFFSET :offset
''', 
                            category=category,
                            offset=offset)
        return [Product(*row) for row in rows]

#this a list of product names
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
    def addProduct(seller_id, name, description, category, image, price, available_quantity):
        try:
            rows = app.db.execute("""
INSERT INTO Products(seller_id, name, description, category, image,
price, available_quantity)
VALUES(:seller_id, :name, :description, :category, :image, :price, :available_quantity)
RETURNING id
""",
                                  seller_id = seller_id,
                                  name = name,
                                  description = description,
                                  category = category,
                                  image=image,
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
price, available_quantity
FROM Products
WHERE lower(name) LIKE '%' || lower(:searchValue) || '%'
''', 
                            searchValue=searchValue)
        return [Product(*row) for row in rows]

# search for product given product name for a specific seller
    @staticmethod
    def search_seller_products(seller_id, searchValue):
        rows = app.db.execute('''
SELECT id, seller_id, name, description, category, image,
price, available_quantity
FROM Products
WHERE lower(name) LIKE '%' || lower(:searchValue) || '%'
AND seller_id = :seller_id
''', 
                            searchValue=searchValue,
                              seller_id = seller_id)
        return [Product(*row) for row in rows]

