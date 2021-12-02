from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    sellers = Product.get_sellers()
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           sellers=sellers)

@bp.route('/sortedindex/<sortoption>')
def sortedindex(sortoption):
    if sortoption == '1':
        products = Product.get_by_price_asc(True)
    else:
        products = Product.get_by_price_desc(True)

    sellers = Product.get_sellers()
    
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           sellers=sellers)

@bp.route('/categorizedindex/<category>')
def categorizedindex(category):
    if category == '1':
        products = Product.get_by_category(category='clothing')
    elif category == '2':
        products = Product.get_by_category(category='food')
    elif category == '3':
        products = Product.get_by_category(category='gadgets')
    elif category == '4':
        products = Product.get_by_category(category='media')
    elif category == '5':
        products = Product.get_by_category(category='misc')
    else:
        products = Product.get_all(True)

    sellers = Product.get_sellers()
    
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           sellers=sellers)

