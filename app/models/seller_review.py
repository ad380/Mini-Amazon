from flask import current_app as app


class SellerReview:
    def __init__(self, seller_id, buyer_id, rating, title, comment, date):
        self.seller_id = seller_id
        self.buyer_id = buyer_id
        self.rating = rating
        self.title = title
        self.comment = comment
        self.date = date


    @staticmethod
    def get(seller_id, orderby="date DESC"):
        # Returns list of SellerReview objects for given seller_id
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

    @staticmethod
    def get_reviewed_sellers(uid):
        # Returns list of seller_id's of products reviewed by user
        rows = app.db.execute('''
    SELECT seller_id
    FROM SellerReviews
    WHERE buyer_id = :uid
    ''',
                    uid=uid)
        return [row[0] for row in rows] if rows is not None else []

    @staticmethod
    def get_review_from(sid, bid):
        rows = app.db.execute('''
    SELECT *
    FROM SellerReviews
    WHERE seller_id = :sid
    AND buyer_id = :bid
    ''',
                    sid=sid,
                    bid=bid)
        return [SellerReview(*row) for row in rows][0]

    @staticmethod
    def get_review(sid, bid):
        rows = app.db.execute('''
    SELECT seller_id, buyer_id
    FROM SellerReviews
    WHERE seller_id = :sid
    AND buyer_id = :bid
    ''',
                    sid=sid,
                    bid=bid)
        return rows[0][0] if rows[0][0] is not None else None

    @staticmethod
    def add_seller_review(sid, bid, rating=None, title=None, comment=None, date=None):
        # Adds a review for a seller
            
        try:
            rows = app.db.execute("""
    INSERT INTO SellerReviews(seller_id, buyer_id, rating, title, comment, date)
    VALUES(:sid, :bid, :rating, :title, :comment, :date)
    RETURNING seller_id, buyer_id
    """,
                    sid=sid,
                    bid=bid,
                    rating=rating,
                    title=title,
                    comment=comment,
                    date=date)

            seller_id, buyer_id = rows[0][0], rows[0][1]
            return SellerReview.get_review(seller_id, buyer_id)
        except Exception as e:
            print(str(e))
            return None

    def add_seller_review_rating(seller_id):
        # Adds default upvote of 0 for new added review

        try:
            rows = app.db.execute("""
    INSERT INTO SellerReviewsUpvotes(uid, seller_id, buyer_id, vote)
    VALUES(0, :seller_id, 0, 0)
    RETURNING seller_id, buyer_id
    """,
                    seller_id=seller_id,
                    )

            seller_id, buyer_id = rows[0][0], rows[0][1]
            return SellerReview.get_review(seller_id, buyer_id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def edit_seller_review(sid, bid, rating=None, title=None, comment=None, date=None):
        # Edit current user's review for seller
        try:
            rows = app.db.execute("""
    UPDATE SellerReviews
    SET seller_id = :sid, buyer_id = :bid, rating = :rating, 
        title = :title, comment = :comment, date = :date
    WHERE seller_id = :sid
    AND buyer_id = :bid
    RETURNING seller_id, buyer_id
    """,
                    sid=sid,
                    bid=bid,
                    rating=rating,
                    title=title,
                    comment=comment,
                    date=date)

            seller_id, buyer_id = rows[0][0], rows[0][1]
            return SellerReview.get_review(seller_id, buyer_id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def deleteReview(sid, bid):
        try:
            rows = app.db.execute('''
DELETE FROM SellerReviews CASCADE
WHERE seller_id = :sid
AND buyer_id = :bid
RETURNING *
''',
                              sid=sid,
                              bid=bid)
            return rows
        except Exception as e:
            print(f"couldn't delete review {e}")
            return None

    @staticmethod
    def get_upvotes(seller_id, bid):
        # Returns list of review upvotes 
        # given the product_id and buyer_id
        rows = app.db.execute('''
    SELECT sum(vote)
    FROM SellerReviewsUpvotes
    WHERE buyer_id = :bid
    AND seller_id = :seller_id    
    ''',
                    seller_id=seller_id,
                    bid=bid)
        return rows[0][0] if rows[0][0] is not None else 0

    @staticmethod
    def get_votes_from(uid, seller_id, bid):
        # Find all votes for given review based on current user
        rows = app.db.execute('''
    SELECT vote
    FROM SellerReviewsUpvotes
    WHERE uid = :uid
    AND seller_id = :seller_id
    AND buyer_id = :bid
    ''',
                    uid=uid,
                    seller_id=seller_id,
                    bid=bid)
        return rows[0][0] if rows else 0

    @staticmethod
    def update_vote(uid, seller_id, bid, val):
        # Updates vote of user for current review
            
        try:
            rows = app.db.execute("""
    UPDATE SellerReviewsUpvotes
    SET uid = :uid, seller_id = :seller_id, buyer_id = :bid, vote = :val
    WHERE uid = :uid 
    AND seller_id = :seller_id
    AND buyer_id = :bid
    RETURNING uid, seller_id, buyer_id
    """,
                    uid=uid,
                    seller_id=seller_id,
                    bid=bid,
                    val=val)

            uid, seller_id, buyer_id = rows[0][0], rows[0][1], rows[0][2]
            print(rows)
            return SellerReview.get_votes_from(uid, seller_id, buyer_id)
        except Exception as e:
            print(str(e))
            pass

        try:
            rows = app.db.execute("""
    INSERT INTO SellerReviewsUpvotes(uid, seller_id, buyer_id, vote)
    VALUES(:uid, :seller_id, :bid, :val)
    RETURNING uid, seller_id, buyer_id
    """,
                    uid=uid,
                    seller_id=seller_id,
                    bid=bid,
                    val=val)

            uid, seller_id, buyer_id = rows[0][0], rows[0][1], rows[0][2]
            return SellerReview.get_votes_from(uid, seller_id, buyer_id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def get_top_reviews(seller_id):
        # Returns list of SellerReview objects for given seller
        rows = app.db.execute(f'''
    SELECT buyer_id
    FROM SellerReviewsUpvotes
    WHERE seller_id = :seller_id
    GROUP BY buyer_id
    ORDER BY sum(vote) DESC
    ''',
                    seller_id=seller_id)

        
        return [SellerReview.get_review_from(seller_id, bid[0]) for bid in rows]
