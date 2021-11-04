from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('products', __name__)


@bp.route('/products/<pid>')
def products(pid):
    product = Product.get(pid)
    return render_template('detailed_product.html', 
                            pid=pid,
                            prod_desc=product.description,
                            prod_name=product.name,
                            prod_price=product.price,
                            prod_quant=product.available_quantity)
