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
    submit = SubmitField('Search')

@bp.route('/inventory',methods=["POST", "GET"])
def index():
    form = SearchForm()
    # get all available products for sale:
    products = Product.get_some()
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
    else:
        purchases = None
        products = None
    # render the page by adding information to the inventory.html file
    if request.method == 'POST':
        purchases = Purchase.search_all_by_seller_id(current_user.id, form.searchValue.data)
        return render_template('orders.html',
                           sold_products=products,
                           purchase_history=purchases,
                           users = users, form = form)
    return render_template('orders.html',
                           sold_products=products,
                           purchase_history=purchases,
                           users = users, form = form)

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
            return redirect(url_for('inventory.index'))
    #render page by adding information to editstatus.html
    return render_template('editstatus.html', title='Edit Purchase Status',
                           form=form, purchase = Purchase.get(pid))
