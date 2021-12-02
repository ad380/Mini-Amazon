from flask import render_template, redirect, url_for, flash, request
from flask.templating import render_template_string
from flask_login import current_user
import datetime


from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired
from flask_babel import _, lazy_gettext as _l

# from app.models.product_review import ProductReview

from .models.product import Product
from .models.purchase import Purchase
from .models.category import Category
from .models.product_review import ProductReview
from .models.user import User

from flask import Blueprint
bp = Blueprint('products', __name__)


@bp.route('/products/<pid>')
def products(pid):
    product = Product.get(pid)
    reviews = ProductReview.get(pid)
    reviewer_ids = [r.buyer_id for r in reviews]
    reviewer_names = [User.get_name(id) for id in reviewer_ids]
    review_count = ProductReview.get_count(pid)
    review_avg = round(ProductReview.get_avg(pid), 1)
    stars = ProductReview.get_stars(review_avg)
    return render_template('detailed_product.html', 
                            pid=pid,
                            prod_desc=product.description,
                            prod_name=product.name,
                            prod_price=product.price,
                            prod_cat=product.category,
                            prod_quant=product.available_quantity,
                            prod_seller=product.seller_id,
                            reviews=reviews,
                            reviewer_names=reviewer_names,
                            review_count=review_count,
                            review_avg=review_avg,
                            stars=stars)

class ProductForm(FlaskForm):
    categories = ['food','clothing','gadgets','media','misc']
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    price = DecimalField(_l('Price', validators=[InputRequired()]))
    description = StringField(_l('Product Description'), validators=[DataRequired()])
    category = SelectField(u'Category', choices = categories, validators = [DataRequired()])
    quantity = IntegerField(_l('Quantity',validators=[InputRequired()]))
    submit = SubmitField(_l('Add to Inventory'))


@bp.route('/products/add', methods=['GET', 'POST'])
def addProduct():
    if current_user.is_authenticated:
        form = ProductForm()
        if form.validate_on_submit():
            if Product.addProduct(current_user.id,
                                  form.name.data,
                                  form.description.data,
                                  form.category.data,
                                  form.price.data,
                                  form.quantity.data):
                flash('Congratualtions, your product has been added')
                return redirect(url_for('inventory.index'))
    return render_template('addproduct.html', title='Add Product', form=form)

class QuantityForm(FlaskForm):
    newQuantity = IntegerField(_l('Quantity',validators=[InputRequired()]))
    submit = SubmitField(_l('Update Quantity'))

@bp.route('/products/edit/<pid>',methods=["POST", "GET"])
def editQuantity(pid):
    quantity = Product.get(pid).available_quantity
    form = QuantityForm()
    form.newQuantity.data = quantity
    if form.validate_on_submit():
        if Product.editQuantity(pid, form.newQuantity.data):
            flash('Congratualtions, your product quantity has been updated')
            return redirect(url_for('inventory.index'))
    return render_template('editquantity.html', title='Edit Product Quantity',
                           form=form, product = Product.get(pid))

class DeleteForm(FlaskForm):
    submit = SubmitField(_l('Delete Product'))
    
@bp.route('/products/delete/<pid>',methods=["POST", "GET"])
def deleteProduct(pid):
    form = DeleteForm()
    if form.validate_on_submit():
        if Product.deleteProduct(pid):
            flash('Your product has been removed')
            return redirect(url_for('inventory.index'))
        return redirect(url_for('inventory.index'))
    return render_template('deleteproduct.html', title='Delete Product',
                           form=form, product = Product.get(pid))

