from flask import current_app as app


class SellerReview:
    def __init__(self, seller_id, buyer_id, rating, comment, date, upvotes):
        self.seller_id = seller_id
        self.buyer_id = buyer_id
        self.rating = rating
        self.comment = comment
        self.date = date
        self.upvotes = upvotes


    @staticmethod
    def get(seller_id, orderby="date DESC"):
        # Returns list of SellerReview objects for given product
        rows = app.db.execute(f'''
    SELECT *
    FROM SellerReviews
    WHERE seller_id = :seller_id
    ORDER BY {orderby}
    ''',
                    seller_id=seller_id)
        return [SellerReview(*row) for row in rows]

    @staticmethod
    def get_count(seller_id):
        # Returns count of reviews for seller_id
        rows = app.db.execute('''
    SELECT count(buyer_id)
    FROM SellerReviews
    WHERE seller_id = :seller_id
    ''',
                    seller_id=seller_id)
        # return [row[0] for row in rows
        return rows[0][0]

    @staticmethod
    def get_avg(seller_id):
        # Returns average of reviews for seller_id
        rows = app.db.execute('''
    SELECT AVG(rating)
    FROM SellerReviews
    WHERE seller_id = :seller_id
    ''',
                    seller_id=seller_id)
        # return [row[0] for row in rows
        return rows[0][0] if rows is not None else 0

    @staticmethod
    def get_user_reviews(uid):
        # Returns list of ratings/reviews authored by user
        # uid in reverse chron order
        rows = app.db.execute('''
    SELECT *
    FROM SellerReviews
    WHERE buyer_id = :uid    
    ORDER BY date DESC
    ''',
                    uid=uid)
        return [SellerReview(*row) for row in rows]