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
        return [row[0] for row in rows] if rows is not None else []

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

        # If user does not add an image to their review,
        # Make default value of "IMAGE"
        if not image:
            image = "IMAGE"
            
        try:
            rows = app.db.execute("""
    INSERT INTO ProductReviews(product_id, buyer_id, rating, title, comment, date, image)
    VALUES(:pid, :bid, :rating, :title, :comment, :date, :image)
    RETURNING product_id, buyer_id
    """,
                    pid=pid,
                    bid=bid,
                    rating=rating,
                    title=title,
                    comment=comment,
                    date=date,
                    image=image)

            product_id, buyer_id = rows[0][0], rows[0][1]
            return ProductReview.get_review(product_id, buyer_id)
        except Exception as e:
            print(str(e))
            return None

    def add_product_review_rating(pid):
        # Adds a review to a product's review

        try:
            rows = app.db.execute("""
    INSERT INTO ProductReviewsUpvotes(uid, product_id, buyer_id, vote)
    VALUES(0, :pid, 0, 0)
    RETURNING product_id, buyer_id
    """,
                    pid=pid,
                    )

            product_id, buyer_id = rows[0][0], rows[0][1]
            return ProductReview.get_review(product_id, buyer_id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def edit_product_review(pid, bid, rating=None, title=None, comment=None, date=None, image=None):
        # Edit current user's review for product pid

        # If user does not add an image to their review,
        # Make default value of "IMAGE"
        if not image:
            image = "IMAGE"
            
        try:
            rows = app.db.execute("""
    UPDATE ProductReviews
    SET product_id = :pid, buyer_id = :bid, rating = :rating, 
        title = :title, comment = :comment, date = :date, image = :image
    WHERE product_id = :pid
    AND buyer_id = :bid
    RETURNING product_id, buyer_id
    """,
                    pid=pid,
                    bid=bid,
                    rating=rating,
                    title=title,
                    comment=comment,
                    date=date,
                    image=image)

            product_id, buyer_id = rows[0][0], rows[0][1]
            return ProductReview.get_review(product_id, buyer_id)
        except Exception as e:
            print(str(e))
            return None
    
    @staticmethod
    def get_review_from(pid, bid):
        rows = app.db.execute('''
    SELECT *
    FROM ProductReviews
    WHERE product_id = :pid
    AND buyer_id = :bid
    ''',
                    pid=pid,
                    bid=bid)
        return [ProductReview(*row) for row in rows][0]

    @staticmethod
    def deleteReview(pid, bid):
        try:
            rows = app.db.execute('''
DELETE FROM ProductReviews CASCADE
WHERE product_id = :pid
AND buyer_id = :bid
RETURNING *
''',
                              pid=pid,
                              bid=bid)
            return rows
        except Exception as e:
            print(f"couldn't delete product: {e}")
            return None

    @staticmethod
    def get_votes_from(uid, pid, bid):
        # Find all votes for given review based on current user
        rows = app.db.execute('''
    SELECT vote
    FROM ProductReviewsUpvotes
    WHERE uid = :uid
    AND product_id = :pid
    AND buyer_id = :bid
    ''',
                    uid=uid,
                    pid=pid,
                    bid=bid)
        return rows[0][0] if rows else 0


    @staticmethod
    def update_vote(uid, pid, bid, val):
        # Updates vote of user for current review
            
        try:
            rows = app.db.execute("""
    UPDATE ProductReviewsUpvotes
    SET uid = :uid, product_id = :pid, buyer_id = :bid, vote = :val
    WHERE uid = :uid 
    AND product_id = :pid
    AND buyer_id = :bid
    RETURNING uid, product_id, buyer_id
    """,
                    uid=uid,
                    pid=pid,
                    bid=bid,
                    val=val)

            uid, product_id, buyer_id = rows[0][0], rows[0][1], rows[0][2]
            print(rows)
            return ProductReview.get_votes_from(uid, product_id, buyer_id)
        except Exception as e:
            print(str(e))
            pass

        try:
            rows = app.db.execute("""
    INSERT INTO ProductReviewsUpvotes(uid, product_id, buyer_id, vote)
    VALUES(:uid, :pid, :bid, :val)
    RETURNING uid, product_id, buyer_id
    """,
                    uid=uid,
                    pid=pid,
                    bid=bid,
                    val=val)

            uid, product_id, buyer_id = rows[0][0], rows[0][1], rows[0][2]
            return ProductReview.get_votes_from(uid, product_id, buyer_id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def get_top_reviews(product_id):
        # Returns list of ProductReview objects for given product
        rows = app.db.execute(f'''
    SELECT buyer_id
    FROM ProductReviewsUpvotes
    WHERE product_id = :product_id
    GROUP BY buyer_id
    ORDER BY sum(vote) DESC
    ''',
                    product_id=product_id)

        
        return [ProductReview.get_review_from(product_id, bid[0]) for bid in rows]
