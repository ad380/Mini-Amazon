from flask import render_template, redirect, url_for, flash, request, Blueprint, session
from flask import current_app as app
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired
from flask_babel import _, lazy_gettext as _l

from app.models.product_review import ProductReview
from app.models.seller_review import SellerReview

from .models.user import User

# imports I've added beyond the skeleton
from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart
from datetime import datetime
import psycopg2
import psycopg2.extras
import os

bp = Blueprint('cart', __name__)

@bp.route('/cart', methods=['GET'])
def carts():
    items = Cart.get(current_user.id)
    total_price = 0
    for item in items:
        total_price += (item.price * item.quantity)
    if len(items) == 0:
        return render_template('empty_cart.html', title='Cart')
    else:
        return render_template('cart.html', title='Cart', user_cart=items, total_price=total_price)

@bp.route('/add', methods=['GET', 'POST'])
def add_to_cart():
    buyer_id = current_user.id
    pid = request.form['pid']

    quantity = 1
    Cart.add_to_cart(buyer_id, pid, quantity)
    return redirect(url_for('cart.carts'))

@bp.route('/inc', methods=['GET', 'POST'])
def inc_quantity():
    pid = request.form['pid']
    curr_quantity = int(request.form['quantity'])
    curr_quantity += 1
    Cart.change_quantity(current_user.id, pid, str(curr_quantity))
    return redirect(url_for('cart.carts'))

@bp.route('/dec', methods=['GET', 'POST'])
def dec_quantity():
    pid = request.form['pid']
    curr_quantity = int(request.form['quantity'])
    curr_quantity -= 1
    if curr_quantity==0:
        Cart.remove_item(current_user.id, pid)
    else:
        Cart.change_quantity(current_user.id, pid, str(curr_quantity))
    return redirect(url_for('cart.carts'))

@bp.route('/remove', methods=['GET', 'POST'])
def remove_item():
    pid = request.form['pid']
    Cart.remove_item(current_user.id, pid)
    return redirect(url_for('cart.carts'))

@bp.route('/submitted', methods=['GET', 'POST'])
def submit_order():
    order = Cart.get(current_user.id)
    total_price = request.form['total']
    #check user balance and inventory
    if float(User.get(current_user.id).balance) < float(total_price):
        return render_template('declined.html')
    for o in order:
        if int(o.quantity) > int(Product.get(o.product_id).available_quantity):
            return render_template('out_of_stock.html')
    

    #if successful:
    ###delete/pop users cart
    Cart.delete(current_user.id)
    ###send items to purchases
    Cart.record_order(order, current_user.id, datetime.now(), Cart.get_last_purchase_id())
    ###decrement balance from buyer and increment for seller
    Cart.payment(current_user.id, total_price)
    Cart.deposit(order)
    ###decrement quantities for each product's available_quantity
    Cart.update_inventory(order)

    return render_template('submitted.html', title='Order Submitted', user_cart=order, total_price=total_price)