from flask import current_app as app

class Cart:
    def __init__(self, buyer_id, product_id, quantity, seller_id, name, image, price, available_quantity):
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.quantity = quantity
        self.seller_id = seller_id
        self.name = name
        self.image = image
        self.price = price
        self.available_quantity = available_quantity

    @staticmethod
    def get(buyer_id):
        rows = app.db.execute("""
        SELECT buyer_id,product_id,quantity, seller_id, name, image, price, available_quantity
        FROM Cart
        INNER JOIN Products ON Products.id=Cart.product_id
        WHERE buyer_id = :buyer_id
        """, buyer_id=buyer_id)
        return rows

    @staticmethod
    def add_to_cart(buyer_id, pid, quantity):
        try:
            app.db.execute("""
    INSERT INTO Cart(buyer_id, product_id, quantity)
    VALUES(:buyer_id, :pid, :quantity)
    """,
                                    buyer_id = buyer_id,
                                    pid = pid,
                                    quantity = quantity)
        except Exception as e:
            print(e)
            print("Couldn't add product to cart")
            return None

    @staticmethod
    def delete(buyer_id):
        try:
            rows = app.db.execute("""
            DELETE FROM Cart
            WHERE buyer_id=:buyer_id
            RETURNING *
            """, buyer_id=buyer_id)
            return rows
        except Exception:
            print("Couldn't delete items from user cart")
            return None

    @staticmethod
    def remove_item(buyer_id, pid):
        try:
            app.db.execute("""
            DELETE FROM Cart
            WHERE buyer_id=:buyer_id AND product_id=:pid
            """,        
                    buyer_id=buyer_id,
                    pid=pid)
        except Exception as e:
            print(e)
            print("Couldn't delete item from cart")

    @staticmethod
    def change_quantity(buyer_id, pid, new):
        try:
            app.db.execute("""
            UPDATE Cart
            SET quantity = :new
            WHERE buyer_id=:buyer_id AND product_id=:pid
            """, buyer_id=buyer_id, pid=pid, new=new)
        except Exception as e:
            print("Couldn't change quantity")

    @staticmethod
    def payment(buyer_id, total_price):
        try:
            app.db.execute("""
            UPDATE Users
            SET balance=balance - :total_price
            WHERE id = :buyer_id
            """,
                                  total_price=total_price,
                                  buyer_id=buyer_id
                                  )
        except Exception:
            print("You don't have enough funds")

    @staticmethod
    def deposit(order):
        for o in order:
            print(o)
            try:
                app.db.execute("""
                UPDATE Users
                SET balance=balance + :deposit
                WHERE id = :seller_id
                """,
                                deposit = o.price * o.quantity,
                                seller_id = o.seller_id)
            except Exception as e:
                print(e)
                print("There was an error in this deposit")

    @staticmethod
    def update_inventory(order):
        for o in order:
            try:
                app.db.execute("""
                UPDATE Products
                SET available_quantity = available_quantity - :quantity
                WHERE id = :product_id
                """,
                                quantity = o.quantity,
                                product_id = o.product_id
                )
            except Exception as e:
                print(e)
                print("There aren't enough available quantities left")

    @staticmethod
    def get_last_purchase_id():
        try:
            rows = app.db.execute("""
            SELECT MAX(id)
            FROM Purchases
            """)
            return int(rows[0][0])
        except Exception as e:
            print(e)
            print('Could not fetch last product id')
            return None

    @staticmethod
    def record_order(order, buyer_id, time, purchase_id):
        for o in order:
            purchase_id += 1
            try:
                app.db.execute("""
                INSERT INTO Purchases(id, uid, seller_id, time_purchased, pid, quantity, fulfilled)
                VALUES(:id, :uid, :seller_id, :time_purchased, :pid, :quantity, :fulfilled)
                """,
                            id = purchase_id,
                            uid = buyer_id,
                            seller_id = o.seller_id,
                            time_purchased = time,
                            pid = o.product_id,
                            quantity = o.quantity,
                            fulfilled = 'nf')
            except Exception as e:
                print('Could not add products to purchases')