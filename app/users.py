from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired
from flask_babel import _, lazy_gettext as _l

from app.models.product_review import ProductReview

from .models.user import User

# imports I've added
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

# stuff I've added:

# make the user profile
@bp.route('/profile')
def profile():
    # get all available products for sale:
    products = Product.get_all(True)
    sellers = Product.get_sellers()
    uid = current_user.id
    reviews = ProductReview.get_user_reviews(uid)
    reviews_pids = [r.product_id for r in reviews]
    prod_names = [Product.get_names(pid) for pid in reviews_pids]
    print(f"names = {prod_names}")
    # find the products and purchases with the current user as the buyer:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the userprofile.html file
    return render_template('userprofile.html',
                           avail_products=products,
                           purchase_history=purchases,
                           sellers=sellers,
                           reviews=reviews,
                           prod_names=prod_names)

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
                flash('Congratulations, your information has been updated!')
                return redirect(url_for('users.profile'))
        return render_template('edituser.html', title='Edit User', form=form)