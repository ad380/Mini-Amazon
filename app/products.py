from flask import render_template, redirect, url_for, flash, request
from flask.templating import render_template_string
from flask_login import current_user
import datetime
from datetime import datetime
import decimal
from decimal import ROUND_HALF_UP


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


@bp.route('/products/<pid>/<sortoption>')
def products(pid, sortoption=0):
    product = Product.get(pid)

    if sortoption == '0':
        order = "date DESC"
    elif sortoption == '1':
        order = "rating DESC"
    else:
        order = "rating ASC"
    reviews = ProductReview.get(pid, orderby=order)
    reviewer_ids = [r.buyer_id for r in reviews]
    reviewer_names = [User.get_name(id) for id in reviewer_ids]
    review_count = ProductReview.get_count(pid)
    review_avg = round(ProductReview.get_avg(pid), 1)

    review_keys = [(r.product_id, r.buyer_id) for r in reviews]
    review_upvotes = [ProductReview.get_upvotes(pid, bid) for pid, bid in review_keys]

    has_purchased = False
    has_reviewed = False
    current_user_review = None
    current_user_name = None
    if current_user.is_authenticated:
        purchases = Purchase.get_all_pid_by_uid(current_user.id)
        reviewedProducts = ProductReview.get_reviewed_products(current_user.id)
        current_user_name = User.get_name(current_user.id)
        if int(pid) in purchases: 
            has_purchased = True
        else:
            has_purchased = False
        if int(pid) in reviewedProducts:
            has_reviewed = True
            current_user_review = ProductReview.get_review_from(pid, current_user.id)
            print(f"current_user_review = {current_user_review}")
        else:
            has_reviewed = False

    return render_template('detailed_product.html', 
                            pid=pid,
                            prod_desc=product.description,
                            prod_name=product.name,
                            prod_price=product.price,
                            prod_cat=product.category,
                            prod_quant=product.available_quantity,
                            prod_seller=product.seller_id,
                            prod_image=product.image,
                            reviews=reviews,
                            reviewer_names=reviewer_names,
                            review_count=review_count,
                            review_avg=review_avg,
                            sortoption=sortoption,
                            review_upvotes=review_upvotes,
                            has_purchased=has_purchased,
                            has_reviewed=has_reviewed,
                            current_user_review=current_user_review,
                            current_user_name=current_user_name)

class ProductForm(FlaskForm):
    categories = ['food','clothing','gadgets','media','misc']
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    price = DecimalField(_l('Price', validators=[InputRequired()]))
    description = StringField(_l('Product Description'), validators=[DataRequired()])
    category = SelectField(u'Category', choices = categories, validators = [DataRequired()])
    quantity = IntegerField(_l('Quantity',validators=[InputRequired()]))
    image = StringField(_l('Image URL'), validators=[DataRequired()])
    submit = SubmitField(_l('Add to Inventory'))

class ReviewForm(FlaskForm):
    rating = DecimalField(_l('Rating (0-5)', places=1, rounding=decimal.ROUND_HALF_UP, validators=[InputRequired()]))
    title = StringField('Title', default=None, validators=[InputRequired()])
    comment = StringField('Comment', default=None, validators=[InputRequired()])
    image = StringField('Image URL (Optional)', default=None)
    submit = SubmitField(_l('Post Review'))

@bp.route('/products/review/<pid>',methods=["GET", "POST"])
def reviewProduct(pid):
    
    if current_user.is_authenticated:
        form = ReviewForm()
        if form.validate_on_submit():
            now = datetime.now()    
            if ProductReview.add_product_review(pid, 
                                            current_user.id, 
                                            form.rating.data, 
                                            form.title.data, 
                                            form.comment.data, 
                                            now.strftime("%b %d, %Y %H:%M:%S"), 
                                            form.image.data):
                print("got here")
                
                return redirect(url_for('products.products', pid=pid, sortoption=0))

    flash('Please make sure your rating value is between 0 and 5.')
    return render_template('reviewProduct.html', title='Title Goes Here',
                           form=form, product = Product.get(pid))


@bp.route('/products/editreview/<pid>',methods=["GET", "POST"])
def editProductReview(pid):
    
    if current_user.is_authenticated:
        form = ReviewForm()
        if form.validate_on_submit():
            now = datetime.now()    
            if ProductReview.edit_product_review(pid, 
                                            current_user.id, 
                                            form.rating.data, 
                                            form.title.data, 
                                            form.comment.data, 
                                            now.strftime("%b %d, %Y %H:%M:%S"), 
                                            form.image.data):
                print("got here")
                
                return redirect(url_for('products.products', pid=pid, sortoption=0))

    flash('Please make sure your rating value is between 0 and 5.')
    return render_template('editProductReview.html', title='Title Goes Here',
                           form=form, product = Product.get(pid))


@bp.route('/products/add', methods=['GET', 'POST'])
def addProduct():
    if current_user.is_authenticated:
        form = ProductForm()
        if form.validate_on_submit():
            if Product.addProduct(current_user.id,
                                  form.name.data,
                                  form.description.data,
                                  form.category.data,
                                  form.image.data,
                                  form.price.data,
                                  form.quantity.data):
                print('Congratualtions, your product has been added')
                return redirect(url_for('inventory.index'))
    return render_template('addproduct.html', title='Add Product', form=form)

class QuantityForm(FlaskForm):
    newQuantity = IntegerField(_l('Quantity',validators=[InputRequired()]))
    submit = SubmitField(_l('Update Quantity'))

@bp.route('/products/edit/<pid>',methods=["POST", "GET"])
def editQuantity(pid):
    quantity = Product.get(pid).available_quantity
    form = QuantityForm()
    form.newQuantity.default = quantity
    if form.validate_on_submit():
        if Product.editQuantity(pid, form.newQuantity.data):
            print('Congratualtions, your product quantity has been updated')
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
            print('Your product has been removed')
            return redirect(url_for('inventory.index'))
        return redirect(url_for('inventory.index'))
    return render_template('deleteproduct.html', title='Delete Product',
                           form=form, product = Product.get(pid))

@bp.route('/products/deletereview/<pid>/<bid>',methods=["POST", "GET"])
def deleteReview(pid, bid):
    if ProductReview.deleteReview(pid, bid):
            print('Your review has been removed')
            return redirect(url_for('products.products', pid=pid, sortoption=0))
    return redirect(url_for('products.products', pid=pid, sortoption=0))

