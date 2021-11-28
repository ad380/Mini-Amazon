from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired
from flask_babel import _, lazy_gettext as _l

from app.models.product_review import ProductReview
from app.models.seller_review import SellerReview

from .models.user import User

# imports I've added beyond the skeleton
from .models.product import Product
from .models.purchase import Purchase
import datetime


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    address = StringField(_l('Address'), validators=[DataRequired()])
    submit = SubmitField(_l('Register'))

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError(_('Already a user with this email.'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

# code I've added beyond the skeleton

# make the private user profile with ability to sort purchases
@bp.route('/sortedprofile/<sortoption>')
def sortedprofile(sortoption):
    # get all available products for sale:
    products = Product.get_all(True)
    sellers = Product.get_sellers()
    uid = current_user.id

    prod_reviews = ProductReview.get_user_reviews(uid)
    reviews_pids = [r.product_id for r in prod_reviews]
    prod_names = [Product.get_names(pid) for pid in reviews_pids]
   
    seller_reviews = SellerReview.get_user_reviews(uid)
    seller_ids = [r.seller_id for r in seller_reviews]
    seller_names = [User.get_name(id) for id in seller_ids]

    # find the products and purchases with the current user as the buyer:
    if current_user.is_authenticated:
        if sortoption == '0':       # sort by date purchased, descending
            purchases = Purchase.get_all_by_uid_since(
                current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        elif sortoption == '1':     # sort by date purchased, ascending
            purchases = Purchase.get_all_by_uid_since_asc(
                current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        elif sortoption == '2':     # sort by purchase id
            purchases = Purchase.get_all_by_uid_since_by_id(
                current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        elif sortoption == '3':     # sort by product id
            purchases = Purchase.get_all_by_uid_since_by_pid(
                current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        elif sortoption == '4':     # sort by seller id
            purchases = Purchase.get_all_by_uid_since_by_seller_id(
                current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        else: # if an invalid sortoption is passed, sort by date purchased, descending
            purchases = Purchase.get_all_by_uid_since(
                current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the userprofile.html file
    return render_template('userprofile.html',
                           avail_products=products,
                           purchase_history=purchases,
                           sellers=sellers,
                           prod_reviews=prod_reviews,
                           prod_names=prod_names,
                           seller_reviews=seller_reviews,
                           seller_names=seller_names)

# make the public user profile
@bp.route('/publicprofile/<uid>')
def privateprofile(uid):
    # get all available products for sale:
    products = Product.get(uid)
    user = User.get(uid)
    sellers = Product.get_sellers()

    reviews = SellerReview.get(uid)
    print(f"reviews = {reviews}")
    reviews_count = SellerReview.get_count(uid)
    # review_avg = round(SellerReview.get_avg(uid), 1)
    avg = SellerReview.get_avg(uid)
    review_avg = 0
    if avg is not None:
        review_avg = round(avg, 1)
    # reviews = ProductReview.get(0)
    # reviews_pids = [r.product_id for r in reviews]
    # prod_names = [Product.get_names(pid) for pid in reviews_pids]

    # render the page by adding information to the publicprofile.html file
    return render_template('publicprofile.html',
                           avail_products=products,
                           sellers=sellers,
                           reviews=reviews,
                           review_count=reviews_count,
                           review_avg=review_avg,
                           user=user)

# make the edit user form
class EditUserForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    address = StringField(_l('Address'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    balance = DecimalField(_l('Balance'), validators=[InputRequired()])
    submit = SubmitField(_l('Update'))

    #can either be a new email that is not taken by someone else or your current email
    def validate_email(self, email):
        if User.email_exists(email.data) and email != self.email:
            raise ValidationError(_('Already a user with this email.'))

# run the edit user form
@bp.route('/edituser', methods=['GET', 'POST'])
def edituser():
    if current_user.is_authenticated:
        form = EditUserForm()
        if form.validate_on_submit():
            if User.edituser(current_user.id,
                            form.email.data,
                            form.password.data,
                            form.firstname.data,
                            form.lastname.data,
                            form.address.data,
                            form.balance.data):
                return redirect(url_for('users.profile'))
        return render_template('edituser.html', title='Edit User', form=form)