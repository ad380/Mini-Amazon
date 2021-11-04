from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('inventory', __name__)


@bp.route('/inventory')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products and purchases with the current user as the seller:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_seller_id(current_user.id)
        products = Product.get_all_by_seller(current_user.id)
    else:
        purchases = None
        products = None
    # render the page by adding information to the index.html file
    return render_template('inventory.html',
                           avail_products=products,
                           purchase_history=purchases)
