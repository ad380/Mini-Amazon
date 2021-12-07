from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, seller_id, time_purchased, pid, quantity,\
                 fulfilled, pname = None, bfname = None, blname = None, baddress = None):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased
        self.seller_id = seller_id
        self.quantity = quantity
        self.fulfilled = fulfilled
        self.pname = pname
        self.bfname = bfname
        self.blname = blname
        self.baddress = baddress

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT Purchases.id, uid, Purchases.seller_id, time_purchased, pid, quantity,
fulfilled, Products.name, Users.firstname, Users.lastname, Users.address
FROM Purchases INNER JOIN Products ON Purchases.pid = Products.id
INNER JOIN Users ON Purchases.uid = Users.id
WHERE Purchases.id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

# get all purchases since the given time/date and in the given order
    @staticmethod
    def get_all_by_uid_ordered(uid, since, orderby="time_purchased DESC"):
        rows = app.db.execute(f'''
SELECT Purchases.id, Purchases.uid, Purchases.seller_id, Purchases.time_purchased, Purchases.pid, Purchases.quantity, Purchases.fulfilled, Products.name
FROM Purchases INNER JOIN Products ON Purchases.pid = Products.id
WHERE Purchases.uid = :uid
AND Purchases.time_purchased >= :since
ORDER BY Purchases.{orderby}
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

#get all product id's of products purchased by user
    @staticmethod
    def get_all_pid_by_uid(uid):
        rows = app.db.execute('''
SELECT pid
FROM Purchases
WHERE uid = :uid
        ''',
                            uid=uid)
        return [row[0] for row in rows]

#returns all purchases of a given seller
    @staticmethod
    def get_all_by_seller_id(seller_id):
        rows = app.db.execute('''
SELECT Purchases.id, uid, Purchases.seller_id, time_purchased, pid, quantity,
fulfilled, Products.name, Users.firstname, Users.lastname, Users.address
FROM Purchases INNER JOIN Products ON Purchases.pid = Products.id
INNER JOIN Users ON Purchases.uid = Users.id
WHERE Purchases.seller_id = :seller_id
ORDER BY time_purchased DESC
''',
                              seller_id=seller_id)
        return [Purchase(*row) for row in rows]

#returns all purchases of a given seller
    @staticmethod
    def get_all_by_seller_id_status(seller_id,status):
        rows = app.db.execute('''
SELECT Purchases.id, uid, Purchases.seller_id, time_purchased, pid, quantity,
fulfilled, Products.name, Users.firstname, Users.lastname, Users.address
FROM Purchases INNER JOIN Products ON Purchases.pid = Products.id
INNER JOIN Users ON Purchases.uid = Users.id
WHERE Purchases.seller_id = :seller_id
AND fulfilled = :status
ORDER BY time_purchased DESC
''',
                              seller_id=seller_id,
                              status = status)
        return [Purchase(*row) for row in rows]

#search for buyer name on all purchases of a given seller
    @staticmethod
    def search_buyer_by_seller_id(seller_id, searchValue):
        rows = app.db.execute('''
SELECT Purchases.id, uid, Purchases.seller_id, time_purchased, pid, quantity,
fulfilled, Products.name, Users.firstname, Users.lastname, Users.address
FROM Purchases INNER JOIN Products ON Purchases.pid = Products.id
INNER JOIN Users ON Purchases.uid = Users.id
WHERE lower(CONCAT(Users.firstname,' ',Users.lastname)) LIKE '%' || lower(:searchValue) || '%'
AND Purchases.seller_id = :seller_id
ORDER BY time_purchased DESC
''',
                              seller_id=seller_id,
                              searchValue = searchValue)
        return [Purchase(*row) for row in rows]

#search for buyer name on all purchases of a given seller filtered by status
    @staticmethod
    def search_buyer_by_seller_id_status(seller_id, searchValue, status):
        rows = app.db.execute('''
SELECT Purchases.id, uid, Purchases.seller_id, time_purchased, pid, quantity,
fulfilled, Products.name, Users.firstname, Users.lastname, Users.address
FROM Purchases INNER JOIN Products ON Purchases.pid = Products.id
INNER JOIN Users ON Purchases.uid = Users.id
WHERE lower(CONCAT(Users.firstname,' ',Users.lastname)) LIKE '%' || lower(:searchValue) || '%'
AND Purchases.seller_id = :seller_id
AND fulfilled = :status
ORDER BY time_purchased DESC
''',
                              seller_id=seller_id,
                              searchValue = searchValue)
        return [Purchase(*row) for row in rows]

#search for product name on all purchases of a given seller
    @staticmethod
    def search_product_by_seller_id(seller_id, searchValue):
        rows = app.db.execute('''
SELECT Purchases.id, uid, Purchases.seller_id, time_purchased, pid, quantity,
fulfilled, Products.name, Users.firstname, Users.lastname, Users.address
FROM Purchases INNER JOIN Products ON Purchases.pid = Products.id
INNER JOIN Users ON Purchases.uid = Users.id
WHERE lower(Products.name) LIKE '%' || lower(:searchValue) || '%'
AND Purchases.seller_id = :seller_id
ORDER BY time_purchased DESC
''',
                              seller_id=seller_id,
                              searchValue = searchValue)
        return [Purchase(*row) for row in rows]

#search for product name on all purchases of a given seller filtered by status
    @staticmethod
    def search_product_by_seller_id_status(seller_id, searchValue, status):
        rows = app.db.execute('''
SELECT Purchases.id, uid, Purchases.seller_id, time_purchased, pid, quantity,
fulfilled, Products.name, Users.firstname, Users.lastname, Users.address
FROM Purchases INNER JOIN Products ON Purchases.pid = Products.id
INNER JOIN Users ON Purchases.uid = Users.id
WHERE lower(Products.name) LIKE '%' || lower(:searchValue) || '%'
AND Purchases.seller_id = :seller_id
AND fulfilled = :status
ORDER BY time_purchased DESC
''',
                              seller_id=seller_id,
                              searchValue = searchValue)
        return [Purchase(*row) for row in rows]


# update purchase status for given purchase id
    @staticmethod
    def editStatus(id, status):
        if status == 'Fulfilled':
            fulfilled = 'f'
        else:
            fulfilled = 'nf'
        try:
            rows = app.db.execute('''
UPDATE Purchases
SET fulfilled = :fulfilled
WHERE id = :id
RETURNING *
''',
                              id=id,
                              fulfilled=fulfilled)
            return rows
        except Exception:
            print("couldn't update purchase status")
            return None

# search for purchases given product name
    @staticmethod
    def search_purchases(searchValue, uid, since):
        rows = app.db.execute('''
SELECT Purchases.id, Purchases.uid, Purchases.seller_id, Purchases.time_purchased, Purchases.pid, Purchases.quantity, Purchases.fulfilled, Products.name
FROM Purchases INNER JOIN Products ON Purchases.pid = Products.id
WHERE lower(Products.name) LIKE '%' || lower(:searchValue) || '%'
AND Purchases.uid = :uid
AND Purchases.time_purchased >= :since
ORDER BY Purchases.time_purchased DESC
''', 
                            searchValue=searchValue,
                            uid=uid,
                            since=since)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_seller_ids_by_uid(uid, seller_id):
        rows = app.db.execute('''
SELECT seller_id
FROM Purchases
WHERE uid = :uid
        ''',
                            uid=uid)
        return [row[0] for row in rows]

    @staticmethod
    def get_seller_id(pid, uid):
        # Returns list of seller_id's of sellers reviewed by user
        rows = app.db.execute('''
    SELECT seller_id
    FROM Purchases
    WHERE uid = :uid
    AND pid = :pid
    ''',
                    uid=uid,
                    pid=pid)
        return rows[0][0] if rows is not None else -1
