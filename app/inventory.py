from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired
from flask_babel import _, lazy_gettext as _l
from .models.product import Product
from .models.purchase import Purchase
from .models.user import User

from flask import Blueprint
bp = Blueprint('inventory', __name__)

#form for searching product name
class SearchForm(FlaskForm):
    searchValue = StringField('', [DataRequired()])
    searchBy = SelectField(u'Search By', choices = ['Buyer Name','Product Name'])
    submit = SubmitField('Search')

@bp.route('/inventory',methods=["POST", "GET"])
def index():
    form = SearchForm()
    # get all available products for sale:
    products = Product.get_all()
    users = User.get_info()
    # find the products and purchases with the current user as the seller:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_seller_id(current_user.id)
        products = Product.get_all_by_seller(current_user.id)
    else:
        purchases = None
        products = None
        
    # render the page by adding information to the inventory.html file based on search
    if request.method == 'POST':
        products = Product.search_seller_products(current_user.id, form.searchValue.data)
        return render_template('inventory.html',
                           sold_products=products,
                           purchase_history=purchases,
                           users = users, form = form)
    return render_template('inventory.html',
                           sold_products=products,
                           purchase_history=purchases,
                           users = users, form = form)

# Order history page
@bp.route('/orders',methods=["POST", "GET"])
def orders():
    form = SearchForm()
    # get all available products for sale:
    products = Product.get_all()
    users = User.get_info()
    # find the products and purchases with the current user as the seller:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_seller_id(current_user.id)
        products = Product.get_all_by_seller(current_user.id)

        status_count = Purchase.count_status(current_user.id)
        labels = ['Fulfilled', 'Not Fulfilled']
        values = []
        for t in status_count:
            l, v = t
            values.append(v)
        print(values)
        
    else:
        purchases = None
        products = None
        labels = None
        values = None
    # render the page by adding information to the inventory.html file
    if request.method == 'POST':
        # if searching by buyer
        if(form.searchBy.data == 'Buyer Name'):
            purchases = Purchase.search_buyer_by_seller_id(current_user.id, form.searchValue.data)
            return render_template('orders.html',
                           sold_products=products,
                           purchase_history=purchases,
                           users = users, form = form, filtered = None, labels = labels, values = values)
        # if searching by product
        else:
            purchases = Purchase.search_product_by_seller_id(current_user.id, form.searchValue.data)
            return render_template('orders.html',
                           sold_products=products,
                           purchase_history=purchases,
                           users = users, form = form, filtered = None, labels = labels, values = values)
    return render_template('orders.html',
                           sold_products=products,
                           purchase_history=purchases,
                           users = users, form = form, filtered = None, labels = labels, values = values)

# Order history page filtered by status
@bp.route('/categorizedorders/<status>', methods = ["POST","GET"])
def ordersByStatus(status):
    form = SearchForm()
    # get all available products for sale:
    products = Product.get_all()
    users = User.get_info()
    
    # find the products and purchases with the current user as the seller:
    if current_user.is_authenticated:
        
        status_count = Purchase.count_status(current_user.id)
        labels = ['Fulfilled', 'Not Fulfilled']
        values = []
        for t in status_count:
            l, v = t
            values.append(v)
        
        #filter by status
        if status == '0':
            if request.method == 'POST':
                # if searching by buyer
                if(form.searchBy.data == 'Buyer Name'):
                    purchases = Purchase.search_buyer_by_seller_id(current_user.id, form.searchValue.data)
                # searching by product
                else:
                    purchases = Purchase.search_product_by_seller_id(current_user.id, form.searchValue.data)
            else:
                purchases = Purchase.get_all_by_seller_id(current_user.id)
        elif status == '1':
            if request.method == 'POST':
                # if searching by buyer
                if(form.searchBy.data == 'Buyer Name'):
                    purchases = Purchase.search_buyer_by_seller_id_status(current_user.id, form.searchValue.data , status='f')
                # searching by product
                else:
                    purchases = Purchase.search_product_by_seller_id_status(current_user.id, form.searchValue.data, status='f')
            else:
                purchases = Purchase.get_all_by_seller_id_status(current_user.id, status='f')
        elif status == '2':
            if request.method == 'POST':
                # if searching by buyer
                if(form.searchBy.data == 'Buyer Name'):
                    purchases = Purchase.search_buyer_by_seller_id_status(current_user.id, form.searchValue.data, status='nf')
                # searching by product
                else:
                    purchases = Purchase.search_product_by_seller_id_status(current_user.id, form.searchValue.data, status='nf')
            else:
                purchases = Purchase.get_all_by_seller_id_status(current_user.id, status='nf')
        else:
            if request.method == 'POST':
                # if searching by buyer
                if(form.searchBy.data == 'Buyer Name'):
                    purchases = Purchase.search_buyer_by_seller_id(current_user.id, form.searchValue.data)
                # searching by product
                else:
                    purchases = Purchase.search_product_by_seller_id(current_user.id, form.searchValue.data)
            else:
                purchases = Purchase.get_all_by_seller_id(current_user.id)
    else:
        purchases = None
        labels = None
        values = None
    # render the page by adding information to the index.html file
    return render_template('orders.html',
                           sold_products=products,
                           purchase_history=purchases,
                           users = users, form = form, filtered = status, labels = labels, values = values)

#Form for editting purchase status
class StatusForm(FlaskForm):
    categories = ['Fulfilled', 'Not Fulfilled']
    newStatus = SelectField(u'Status', choices = categories, validators = [DataRequired()])
    submit = SubmitField(_l('Submit Purchase Status'))

#page to edit purchase status
@bp.route('/editstatus/<pid>',methods=["POST", "GET"])
def editStatus(pid):
    status = Purchase.get(pid).fulfilled
    if status == 'f':
        status = 'Fulfilled'
    else:
        status = 'Not Fulfilled'
    form = StatusForm()
    #set default status as existing value
    form.newStatus.default = status
    if form.validate_on_submit():
        if Purchase.editStatus(pid, form.newStatus.data):
            print('Congratualtions, your purchase status has been updated')
            return redirect(url_for('inventory.orders'))
    #render page by adding information to editstatus.html
    return render_template('editstatus.html', title='Edit Purchase Status',
                           form=form, purchase = Purchase.get(pid))
