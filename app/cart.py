from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from .models.user import User
from .models.product import Product
from .models.purchase import Purchase
from flask import Blueprint

bp = Blueprint('cart', __name__)

@bp.route('/cart')
#def cart():

#    return render_template('cart.html', title='Cart')