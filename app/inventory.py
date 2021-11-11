from flask import render_template
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from .models.product import Product
from .models.purchase import Purchase
from .models.user import User

from flask import Blueprint
bp = Blueprint('inventory', __name__)


@bp.route('/inventory',methods=["POST", "GET"])
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    users = User.get_info()
    # find the products and purchases with the current user as the seller:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_seller_id(current_user.id)
        products = Product.get_all_by_seller(current_user.id)
    else:
        purchases = None
        products = None
    # render the page by adding information to the inventory.html file
    return render_template('inventory.html',
                           sold_products=products,
                           purchase_history=purchases,
                           users = users)
