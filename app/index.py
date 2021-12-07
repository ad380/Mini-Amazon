from flask import render_template
from flask import Flask, render_template, session, redirect, url_for, request
from flask_login import current_user
import datetime

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired
from flask_babel import _, lazy_gettext as _l

from .models.product import Product
from .models.purchase import Purchase
from .models.product_review import ProductReview

from flask import Blueprint
bp = Blueprint('index', __name__)

class SearchForm(FlaskForm):
    searchValue = StringField('', [DataRequired()])
    submit = SubmitField('Search')


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    # get all available products for sale:
    products = Product.get_some()
    product_ids = [p.id for p in products]
    product_avgs = [round(ProductReview.get_avg(id), 1) for id in product_ids]

    sellers = Product.get_sellers()
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_ordered(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    if request.method == 'POST':
        products = Product.search_products(form.searchValue.data)
        print(form.searchValue.data)
        print(len(products))
        return render_template('index.html',
                                avail_products=products,
                                purchase_history=purchases,
                                sellers=sellers,
                                page_num=1,
                                sortoption=0,
                                category=0,
                                form=form,
                                product_avgs=product_avgs)

    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           sellers=sellers,
                           page_num=1,
                           sortoption=0,
                           category=0,
                           form=form,
                           product_avgs=product_avgs)

@bp.route('/sortedindex/<sortoption>/<page_num>')
def sortedindex(sortoption, page_num=1):
    form = SearchForm()
    offset = (int(page_num) - 1) * 100
    if sortoption == '0' or sortoption == '-1':
        products = Product.get_some(offset=offset)
    elif sortoption == '1':
        products = Product.get_by_price_asc(offset)
    elif sortoption == '2':
        products = Product.get_by_price_desc(offset)
    else:
        pids = Product.get_by_rating(offset)
        products = []
        for pid in pids:
            this_product = Product.get(pid)
            products.append(this_product)

    product_ids = [p.id for p in products]
    product_avgs = [round(ProductReview.get_avg(id), 1) for id in product_ids]

    sellers = Product.get_sellers()
    
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_ordered(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           sellers=sellers,
                           page_num=int(page_num),
                           sortoption=int(sortoption),
                           category=0,
                           form=form,
                           product_avgs=product_avgs)

@bp.route('/categorizedindex/<category>/<page_num>')
def categorizedindex(category, page_num):
    form = SearchForm()
    offset = (int(page_num) - 1) * 50
    if category == '0' or category == '-1':
        products = Product.get_some(offset=offset)
    elif category == '1':
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
        products = Product.get_some(offset=offset)

    sellers = Product.get_sellers()

    product_ids = [p.id for p in products]
    product_avgs = [round(ProductReview.get_avg(id), 1) for id in product_ids]
    
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_ordered(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           sellers=sellers,
                           page_num=int(page_num),
                           sortoption=0,
                           category=int(category),
                           form=form,
                           product_avgs=product_avgs)
