from flask import current_app as app


class ProductReview:
    def __init__(self, product_id, buyer_id, rating, comment, upvotes):
        self.product_id = product_id
        self.buyer_id = buyer_id
        self.rating = rating
        self.comment = comment
        self.upvotes = upvotes


    @staticmethod
    def get(product_id):
        # Returns list of ProductReview objects for given product
        rows = app.db.execute('''
    SELECT *
    FROM ProductReviews
    WHERE product_id = :product_id
    ''',
                    product_id=product_id)
        return [ProductReview(*row) for row in rows]