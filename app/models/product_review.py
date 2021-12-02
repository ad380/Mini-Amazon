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
    ORDER BY rating DESC
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
    ORDER BY date DESC
    ''',
                    uid=uid)
        return [ProductReview(*row) for row in rows]

    @staticmethod
    def get_stars(avg, half=False):
        """Return list of size 5 representing how many stars
        should be shown for review
        -1 = empty, 0 = half, 1 = full
        """
        dec = avg % 1 #number after decimal
        full = int(avg) #number before decimal
        tail = [-1 for i in range(4 - full)] #for padding rest of list with 0s

        if 0.25 < dec and dec <= 0.75:
            # When decimal value in this range, we have half star
            half = True

        stars = [1 for i in range(int(avg))]
        if half:
            stars.append(0)
        elif dec < 0.25:
            stars.append(-1)
        else:
            stars.append(1)
        stars += tail

        return stars
        
        
        