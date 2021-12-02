from flask import render_template
from flask.templating import render_template_string
from flask_login import current_user
import datetime


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from app.models.product_review import ProductReview

from .models.product import Product
from .models.purchase import Purchase
from .models.category import Category
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
                            prod_cat=product.category,
                            prod_quant=product.available_quantity,
                            prod_seller=product.seller_id,
                            reviews=reviews,
                            review_count=review_count,
                            review_avg=review_avg)

class ProductForm(FlaskForm):
    categories = Category.get()
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), validators=[DataRequired()])
    description = StringField(_l('Product Description'), validators=[DataRequired()])
    category = SelectField(u'Category', choices = categories, validators = [Required()])
    quantity = IntegerField(_l('Quantity'),validators=[DataRequired()] )
    submit = SubmitField(_l('Add to Inventory'))


@bp.route('/products/add', methods=['GET', 'POST'])
def addProduct():
    if current_user.is_authenticated:
        form = ProductForm()
        if form.validate_on_submit():
            if Product.addProduct(
                                  form.name.data,
                                  form.description.data,
                                  form.category.data,
                                  form.price.data,
                                  form.quantity.data):
                flash('Congratualtions, your product has been added')
                return redirect(url_for('inventory.index'))
            return render_template('addproduct.html', title='Add Product', form=form)
        return render_template('addproduct.html', title='Add Product', form=form)
    return render_template('addproduct.html', title='Add Product', form=form)
