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

# get all purchases since the given time/date and in the given order
    @staticmethod
    def get_all_by_uid_ordered(uid, since, orderby="time_purchased DESC"):
        rows = app.db.execute(f'''
SELECT id, uid, seller_id, time_purchased, pid, quantity, fulfilled
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY {orderby}
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
''',
                              id=id,
                              fulfilled=fulfilled)
            return id
        except Exception:
            print("couldn't update purchase status")
            return None
