from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('products', __name__)


@bp.route('/products/<pid>')
def products(pid):

    return render_template('detailed_product.html', pid=pid)
