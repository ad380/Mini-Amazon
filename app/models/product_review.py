from flask import current_app as app


class ProductReview:
    def __init__(self, product_id, buyer_id, rating, comment, date, upvotes):
        self.product_id = product_id
        self.buyer_id = buyer_id
        self.rating = rating
        self.comment = comment
        self.date = date
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

    @staticmethod
    def get_count(product_id):
        # Returns list of ProductReview objects for given product
        rows = app.db.execute('''
    SELECT count(buyer_id)
    FROM ProductReviews
    WHERE product_id = :product_id
    ''',
                    product_id=product_id)
        # return [row[0] for row in rows
        return rows[0][0]

    @staticmethod
    def get_avg(product_id):
        # Returns list of ProductReview objects for given product
        rows = app.db.execute('''
    SELECT AVG(rating)
    FROM ProductReviews
    WHERE product_id = :product_id
    ''',
                    product_id=product_id)
        # return [row[0] for row in rows
        return rows[0][0]

    @staticmethod
    def get_user_reviews(uid):
        # Returns list of ratings/reviews authored by user
        # uid in reverse chron order
        rows = app.db.execute('''
    SELECT *
    FROM ProductReviews
    WHERE buyer_id = :uid    
    ORDER BY date
    ''',
                    uid=uid)
        return [ProductReview(*row) for row in rows]