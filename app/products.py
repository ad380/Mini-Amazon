from flask import render_template
from flask.templating import render_template_string
from flask_login import current_user
import datetime

from app.models.product_review import ProductReview

from .models.product import Product
from .models.purchase import Purchase
from .models.product_review import ProductReview

from flask import Blueprint
bp = Blueprint('products', __name__)


@bp.route('/products/<pid>')
def products(pid):
    product = Product.get(pid)
    reviews = ProductReview.get(pid)
    review_count = ProductReview.get_count(pid)
    review_avg = round(ProductReview.get_avg(pid), 1)
    return render_template('detailed_product.html', 
                            pid=pid,
                            prod_desc=product.description,
                            prod_name=product.name,
                            prod_price=product.price,
                            prod_quant=product.available_quantity,
                            prod_seller=product.seller_id
                            reviews=reviews,
                            review_count=review_count,
                            review_avg=review_avg)
