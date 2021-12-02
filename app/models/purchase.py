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
SELECT id, uid, seller_id, time_purchased, pid, quantity, fulfilled
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, seller_id, time_purchased, pid, quantity, fulfilled
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

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

# methods Tess has added

# get all purchases by time ascending (chronological)
    @staticmethod
    def get_all_by_uid_since_asc(uid, since):
        rows = app.db.execute('''
SELECT id, uid, seller_id, time_purchased, pid, quantity, fulfilled
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

# get all purchases by purchase id
    @staticmethod
    def get_all_by_uid_since_by_id(uid, since):
        rows = app.db.execute('''
SELECT id, uid, seller_id, time_purchased, pid, quantity, fulfilled
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY id
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

# get all purchases by product id
    @staticmethod
    def get_all_by_uid_since_by_pid(uid, since):
        rows = app.db.execute('''
SELECT id, uid, seller_id, time_purchased, pid, quantity, fulfilled
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY pid
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

# get all purchases by seller_id
    @staticmethod
    def get_all_by_uid_since_by_seller_id(uid, since):
        rows = app.db.execute('''
SELECT id, uid, seller_id, time_purchased, pid, quantity, fulfilled
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY seller_id
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

# update purchase status for given purchase id
    @staticmethod
    def editStatus(id, status):
        if status == 'Fulfilled':
            fulfilled = 'f'
        else:
            fulfilled = 'nf'
            
        rows = app.db.execute('''
UPDATE Purchases
SET fulfilled = :fulfilled
WHERE id = :id
''',
                              id=id,
                              fulfilled=fulfilled)
        return id
