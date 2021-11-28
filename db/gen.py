from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import os
from flask import current_app as app
import random
from datetime import datetime


num_users = 500
num_sellers = 100
num_products = 500
num_purchases = 10000
RATING_VALS = [0, 0.5, 1.0, 1.5, 2.0, 2.5,
            3.0, 3.5, 4.0, 4.5, 5.0]

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def get_categories():
    category_list = []
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f = open(os.path.join(__location__, 'data/Category.csv'))
    with f as csvfile:
        category = csv.reader(csvfile)
        for c in category:
            category_list.append(c[0])
    return category_list

# randomly generate users
def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = profile['address']
            writer.writerow([uid, email, password, firstname, lastname, address, 0.00])
        print(f'{num_users} generated')
    return


def gen_products(num_products):
    available_pids = dict()
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            available_quantity = 0
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            seller_id = fake.random_int(min=0, max=num_sellers-1)
            name = fake.sentence(nb_words=4)[:-1]
            description = fake.bs()
            categories = get_categories()
            category = categories[fake.random_int(min=0, max=len(categories)-1)]
            #TODO: CHANGE IMAGE
            image = "IMAGE"
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids[pid] = (seller_id, price)
                available_quantity = fake.random_int(min=1, max=500)
            writer.writerow([pid, seller_id, name, description, category, image, price, available, available_quantity])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            pid = fake.random_element(elements=available_pids.keys())
            seller_id = available_pids[pid][0]
            uid = fake.random_int(min=0, max=num_users-1)
            while uid == seller_id: # make sure a user doesn't buy product from themself
                uid = fake.random_int(min=0, max=num_users-1)

            time_purchased = fake.date_time_ad(start_datetime=datetime(1980, 9, 14, 0, 0, 0))
            quantity = fake.random_int(min=0, max=100)

            fulfilled = fake.random_element(elements=('f', 'nf'))
            
            # writer.writerow([id, uid, pid, time_purchased])
            writer.writerow([id, uid, seller_id, time_purchased, pid, 
                    quantity, fulfilled])
        print(f'{num_purchases} generated')
    return


def get_random_purchases_ratings():
    ratings = dict()
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f = open(os.path.join(__location__, 'data/Purchases.csv'))
    with f as csvfile:
        purchases = csv.reader(csvfile)
        for purchase in purchases:
            # First check if purchase fulfilled
            id, uid, seller_id, time_purchased, pid, \
                quantity, fulfilled = purchase
            if fulfilled == 'f':
                review_ratio = .5 # review_ratio % of purchases actually contain a review
                if random.random() <= review_ratio:
                    rating = random.choice(RATING_VALS)
                    # ratings.append((pid, uid, rating))
                    ratings[(pid, uid)] = rating
    return ratings


def gen_product_reviews():
    ratings = get_random_purchases_ratings()

    # product_id, buyer_id, rating, comment
    with open('ProductReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        for r in ratings.keys():
            product_id, buyer_id = r
            rating = ratings[r]
            comment = ""
            comment_ratio = .5 # comment_ratio % of ratings actually contain a comment
            if random.random() <= comment_ratio:
                comment = fake.paragraph(nb_sentences=6, variable_nb_sentences=True)
            date = fake.date_time()
            writer.writerow([product_id, buyer_id, rating, comment[:512], date, 0])
    return

def get_random_seller_ratings():
    ratings = dict()
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f = open(os.path.join(__location__, 'data/Purchases.csv'))
    with f as csvfile:
        purchases = csv.reader(csvfile)
        for purchase in purchases:
            # First check if purchase fulfilled
            id, uid, seller_id, time_purchased, pid, quantity, fulfilled = purchase
            if fulfilled == 'f':
                review_ratio = .7 # review_ratio % of purchases actually contain a review
                if random.random() <= review_ratio:
                    rating = random.choice(RATING_VALS)
                    # ratings.append((pid, uid, rating))
                    #dictionary enforces key value constraint
                    ratings[(seller_id, uid)] = (rating, time_purchased)
    return ratings   


def gen_seller_reviews():
    ratings = get_random_seller_ratings()

    # product_id, buyer_id, rating, comment
    with open('SellerReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        for r in ratings.keys():
            seller_id, buyer_id, = r
            rating = ratings[r][0]
            time_purchased = ratings[r][1]
            comment = ""
            comment_ratio = .75 # comment_ratio % of ratings actually contain a comment
            if random.random() <= comment_ratio:
                comment = fake.paragraph(nb_sentences=6, variable_nb_sentences=True)
            # make sure time of seller review happens after product is purchased from that seller
            date = fake.date_time_ad(start_datetime=datetime.fromisoformat(time_purchased))
            writer.writerow([seller_id, buyer_id, rating, comment[:512], date, 0])
    return

# gen_users(num_users)
# available_pids = gen_products(num_products)
# gen_purchases(num_purchases, available_pids)
gen_product_reviews()
gen_seller_reviews()
# print(random.choice(RATINGS))
# print(get_random_seller_ratings())