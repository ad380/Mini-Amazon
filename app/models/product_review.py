from flask import current_app as app


class ProductReview:
    def __init__(self, product_id, buyer_id, rating, title, comment, date, image):
        self.product_id = product_id
        self.buyer_id = buyer_id
        self.rating = rating
        self.title = title
        self.comment = comment
        self.date = date
        self.image = image


    @staticmethod
    def get(product_id, orderby="date DESC"):
        # Returns list of ProductReview objects for given product
        rows = app.db.execute(f'''
    SELECT *
    FROM ProductReviews
    WHERE product_id = :product_id
    ORDER BY {orderby}
    ''',
                    product_id=product_id)
        return [ProductReview(*row) for row in rows]

    @staticmethod
    def get_count(product_id):
        # Returns number of reviews for product
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
        # Returns average rating for product
        rows = app.db.execute('''
    SELECT AVG(rating)
    FROM ProductReviews
    WHERE product_id = :product_id
    ''',
                    product_id=product_id)
        return rows[0][0] if rows[0][0] is not None else 0

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
    def get_reviewed_products(uid):
        # Returns list of product id's of products reviewed by user
        rows = app.db.execute('''
    SELECT product_id
    FROM ProductReviews
    WHERE buyer_id = :uid
    ''',
                    uid=uid)
        return [row[0] for row in rows]

    @staticmethod
    def get_upvotes(pid, bid):
        # Returns list of review upvotes 
        # given the product_id and buyer_id
        rows = app.db.execute('''
    SELECT sum(vote)
    FROM ProductReviewsUpvotes
    WHERE buyer_id = :bid
    AND product_id = :pid    
    ''',
                    pid=pid,
                    bid=bid)
        return rows[0][0] if rows[0][0] is not None else 0
        
    @staticmethod
    def get_review(pid, bid):
        rows = app.db.execute('''
    SELECT product_id, buyer_id
    FROM ProductReviews
    WHERE product_id = :pid
    AND buyer_id = :bid
    ''',
                    pid=pid,
                    bid=bid)
        return rows[0][0] if rows[0][0] is not None else None

    @staticmethod
    def add_product_review(pid, bid, rating=None, title=None, comment=None, date=None, image=None):
        # Adds a review to a product's review
        try:
            rows = app.db.execute("""
    INSERT INTO ProductReviews(product_id, buyer_id, rating, title, comment, date, image)
    VALUES(:pid, :bid, :rating, :title, :comment, :date, :image)
    """,
                    pid=pid,
                    bid=bid,
                    rating=rating,
                    title=title,
                    comment=comment,
                    date=date,
                    image=image)

            print(rows)
            return Product_Review.get_review(pid, bid)
        except Exception:
            print("Couldn't add review")
            return None
    
        
