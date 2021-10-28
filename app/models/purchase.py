from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, seller_id, time_purchased, pid, quantity):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased
        self.seller_id = seller_id
        self.quantity = quantity

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, seller_id, time_purchased, pid, quantity
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, seller_id, time_purchased, pid, quantity
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
SELECT id, uid, seller_id, time_purchased, pid, quantity
FROM Purchases
WHERE seller_id = :seller_id
ORDER BY time_purchased DESC
''',
                              seller_id=seller_id)
        return [Purchase(*row) for row in rows]
