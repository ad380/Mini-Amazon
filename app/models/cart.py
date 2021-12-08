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
            rows = app.db.execute("""
    INSERT INTO Cart(buyer_id, product_id, quantity)
    VALUES(:buyer_id, :pid, :quantity)
    RETURNING product_id
    """,
                                    buyer_id = buyer_id,
                                    pid = pid,
                                    quantity = quantity)
            return Product.get(pid)
        except Exception:
            print("Couldn't add product to cart")
            return None