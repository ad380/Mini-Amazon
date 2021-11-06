from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.user import User

from flask import Blueprint
bp = Blueprint('userprofile', __name__)


@bp.route('/userprofile')
def index():
    # find the products and purchases with the current user as the buyer:
    if current_user.is_authenticated:
        purchases = Purchase.get(current_user.id)
    else:
        purchases = None
    # render the page by adding information to the userprofile.html file
    return render_template('userprofile.html',
                           purchase_history=purchases)