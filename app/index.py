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
    products = Product.get_some()
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

@bp.route('/sortedindex/<sortoption>/<page_num>')
def sortedindex(sortoption, page_num=1):
    offset = (int(page_num) - 1) * 50
    if sortoption == '1':
        products = Product.get_by_price_asc(True, offset)
    else:
        products = Product.get_by_price_desc(True, offset)

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

@bp.route('/categorizedindex/<category>/<page_num>')
def categorizedindex(category, page_num):
    offset = (int(page_num) - 1) * 50
    if category == '1':
        products = Product.get_by_category(category='clothing', offset=offset)
    elif category == '2':
        products = Product.get_by_category(category='food', offset=offset)
    elif category == '3':
        products = Product.get_by_category(category='gadgets', offset=offset)
    elif category == '4':
        products = Product.get_by_category(category='media', offset=offset)
    elif category == '5':
        products = Product.get_by_category(category='misc', offset=offset)
    else:
        products = Product.get_some()

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

