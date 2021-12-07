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
from datetime import datetime

import decimal
from decimal import ROUND_HALF_UP


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

# create the search bar form
class UserSearchForm(FlaskForm):
    searchValue = StringField('', [DataRequired()])
    submit = SubmitField('Search')

# make the private user profile with ability to sort purchases
@bp.route('/profile/<sortoption>', methods=['GET', 'POST'])
def sortedprofile(sortoption='0'):
    # get search bar form
    form = UserSearchForm()

    # get all available products for sale:
    products = Product.get_all()
    sellers = Product.get_sellers()
    uid = current_user.id

    prod_reviews = ProductReview.get_user_reviews(uid)
    reviews_pids = [r.product_id for r in prod_reviews]
    prod_names = [Product.get_names(pid) for pid in reviews_pids]
   
    seller_reviews = SellerReview.get_user_reviews(uid)
    seller_ids = [r.seller_id for r in seller_reviews]
    seller_names = [User.get_name(id) for id in seller_ids]

    # find the products and purchases with the current user as the buyer:
    
    if sortoption == '0':       # sort by date purchased, descending
        order = "time_purchased DESC"
    elif sortoption == '1':     # sort by date purchased, ascending
        order = "time_purchased"
    elif sortoption == '2':     # sort by purchase id
        order = "id"
    elif sortoption == '3':     # sort by product id
        order = "pid"
    elif sortoption == '4':     # sort by seller id
        order = "seller_id"
    elif sortoption == '5':     # sort by seller id
        order = "quantity"
    elif sortoption == '6':     # sort by seller id
        order = "fulfilled DESC"
    else: # if an invalid sortoption is passed, sort by date purchased, descending
        order = "time_purchased DESC"
    
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_ordered(current_user.id, datetime(1980, 9, 14, 0, 0, 0), orderby=order)
    else:
        purchases = None
    
    # render the page by adding information to the userprofile.html file

    # if we are searching product names
    if request.method == 'POST':
        purchases = Purchase.search_purchases(form.searchValue.data, current_user.id, datetime(1980, 9, 14, 0, 0, 0))
        print(form.searchValue.data)
        print(len(purchases))
        return render_template('userprofile.html',
                           avail_products=products,
                           purchase_history=purchases,
                           sellers=sellers,
                           prod_reviews=prod_reviews,
                           prod_names=prod_names,
                           seller_reviews=seller_reviews,
                           seller_names=seller_names,
                           sortoption=sortoption,
                           form=form)

    return render_template('userprofile.html',
                           avail_products=products,
                           purchase_history=purchases,
                           sellers=sellers,
                           prod_reviews=prod_reviews,
                           prod_names=prod_names,
                           seller_reviews=seller_reviews,
                           seller_names=seller_names,
                           sortoption=sortoption,
                           form=form)

# make the public user profile
@bp.route('/publicprofile/<uid>/<sortoption>')
def publicprofile(uid, sortoption=0):
    # get all available products for sale:
    products = Product.get(uid)
    user = User.get(uid)
    sellers = Product.get_sellers()

    if sortoption == '0':
        order = "date DESC"
    elif sortoption == '1':
        order = "rating DESC"
    else:
        order = "rating ASC"

    reviews = SellerReview.get(uid, orderby=order)
    reviewer_ids = [r.buyer_id for r in reviews]
    reviewer_names = [User.get_name(id) for id in reviewer_ids]
    reviews_count = SellerReview.get_count(uid)
    avg = SellerReview.get_avg(uid)
    review_avg = 0
    if avg is not None:
        review_avg = round(avg, 1)

    has_purchased_from, has_reviewed = False, False
    current_user_review, current_user_name = None, None
    if current_user.is_authenticated:
        purchases_ids = Purchase.get_all_pid_by_uid(current_user.id)

        purchased_from = [Purchase.get_seller_id(pid, current_user.id) for pid in purchases_ids]
        reviewedSellers = SellerReview.get_reviewed_sellers(current_user.id)
        current_user_name = User.get_name(current_user.id)

        if int(uid) in set(purchased_from): 
            has_purchased = True
        else:
            has_purchased = False
        if int(uid) in reviewedSellers:
            has_reviewed = True
            current_user_review = SellerReview.get_review_from(uid, current_user.id)
        else:
            has_reviewed = False

    # render the page by adding information to the publicprofile.html file
    return render_template('publicprofile.html',
                           avail_products=products,
                           sellers=sellers,
                           reviews=reviews,
                           review_count=reviews_count,
                           review_avg=review_avg,
                           user=user,
                           sortoption=sortoption,
                           reviewer_names=reviewer_names,
                           has_purchased_from=has_purchased_from,
                           has_reviewed=has_reviewed,
                           current_user_review=current_user_review,
                           current_user_name=current_user_name,
                           has_purchased=has_purchased)

class ReviewForm(FlaskForm):
    rating = DecimalField(_l('Rating (0-5)', places=1, rounding=decimal.ROUND_HALF_UP, validators=[InputRequired()]))
    title = StringField('Title', default=None, validators=[InputRequired()])
    comment = StringField('Comment', default=None, validators=[InputRequired()])
    submit = SubmitField(_l('Post Review'))

@bp.route('/publicprofile/review/<uid>',methods=["GET", "POST"])
def reviewSeller(uid): 
    if current_user.is_authenticated:
        form = ReviewForm()
        if form.validate_on_submit():
            now = datetime.now()    
            if SellerReview.add_seller_review(uid, 
                                            current_user.id, 
                                            form.rating.data, 
                                            form.title.data, 
                                            form.comment.data, 
                                            now.strftime("%b %d, %Y %H:%M:%S")):          
                return redirect(url_for('users.publicprofile', uid=uid, sortoption=0))

    flash('Please make sure your rating value is between 0 and 5.')
    return render_template('reviewSeller.html', 
                            title='Title Goes Here',
                            form=form, 
                            seller_id=uid,
                            seller_name=User.get_name(uid))

@bp.route('/publicprofile/editreview/<uid>',methods=["GET", "POST"])
def editSellerReview(uid): 
    if current_user.is_authenticated:
        form = ReviewForm()
        if form.validate_on_submit():
            now = datetime.now()    
            if SellerReview.edit_seller_review(uid, 
                                            current_user.id, 
                                            form.rating.data, 
                                            form.title.data, 
                                            form.comment.data, 
                                            now.strftime("%b %d, %Y %H:%M:%S")):
                return redirect(url_for('users.publicprofile', uid=uid, sortoption=0))

    flash('Please make sure your rating value is between 0 and 5.')
    return render_template('editSellerReview.html', 
                            title='Title Goes Here',
                            form=form, 
                            seller_id=uid,
                            seller_name=User.get_name(uid))
    

# make the edit name form
class EditNameForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    password = PasswordField(_l('Confirm Password'), validators=[DataRequired()])
    submit = SubmitField(_l('Update'))

# run the edit name form
@bp.route('/editname', methods=['GET', 'POST'])
def editname():
    if current_user.is_authenticated:
        form = EditNameForm()
        if form.validate_on_submit():
            user = User.get_by_auth(current_user.email, form.password.data)
            if user is None:
                print('Invalid password')
                return redirect(url_for('users.editname'))
            if User.edituser(current_user.id,
                            current_user.email,
                            form.password.data,
                            form.firstname.data,
                            form.lastname.data,
                            current_user.address,
                            current_user.balance):
                return redirect(url_for('users.sortedprofile', sortoption=0))
        return render_template('editname.html', title='Edit User Name', form=form)

# make the edit email form
class EditEmailForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Confirm Password'), validators=[DataRequired()])
    submit = SubmitField(_l('Update'))

    #can either be a new email that is not taken by someone else or your current email
    def validate_email(self, email):
        if User.email_exists(email.data) and email != self.email:
            raise ValidationError(_('Already a user with this email.'))

# run the edit name form
@bp.route('/editemail', methods=['GET', 'POST'])
def editemail():
    if current_user.is_authenticated:
        form = EditEmailForm()
        if form.validate_on_submit():
            user = User.get_by_auth(current_user.email, form.password.data)
            if user is None:
                print('Invalid password')
                return redirect(url_for('users.editemail'))
            if User.edituser(current_user.id,
                            form.email.data,
                            form.password.data,
                            current_user.firstname,
                            current_user.lastname,
                            current_user.address,
                            current_user.balance):
                return redirect(url_for('users.sortedprofile', sortoption=0))
        return render_template('editemail.html', title='Edit User Email', form=form)

# make the edit address form
class EditAddressForm(FlaskForm):
    address = StringField(_l('Address'), validators=[DataRequired()])
    password = PasswordField(_l('Confirm Password'), validators=[DataRequired()])
    submit = SubmitField(_l('Update'))

# run the edit address form
@bp.route('/editaddress', methods=['GET', 'POST'])
def editaddress():
    if current_user.is_authenticated:
        form = EditAddressForm()
        if form.validate_on_submit():
            user = User.get_by_auth(current_user.email, form.password.data)
            if user is None:
                print('Invalid password')
                return redirect(url_for('users.editaddress'))
            if User.edituser(current_user.id,
                            current_user.email,
                            form.password.data,
                            current_user.firstname,
                            current_user.lastname,
                            form.address.data,
                            current_user.balance):
                return redirect(url_for('users.sortedprofile', sortoption=0))
        return render_template('editaddress.html', title='Edit User Address', form=form)

# make the edit balance form
class EditBalanceForm(FlaskForm):
    balance = DecimalField(_l('Balance'), validators=[InputRequired()])
    password = PasswordField(_l('Confirm Password'), validators=[DataRequired()])
    submit = SubmitField(_l('Update'))

# run the edit balance form
@bp.route('/editbalance', methods=['GET', 'POST'])
def editbalance():
    if current_user.is_authenticated:
        form = EditBalanceForm()
        if form.validate_on_submit():
            user = User.get_by_auth(current_user.email, form.password.data)
            if user is None:
                print('Invalid password')
                return redirect(url_for('users.editbalance'))
            if User.edituser(current_user.id,
                            current_user.email,
                            form.password.data,
                            current_user.firstname,
                            current_user.lastname,
                            current_user.address,
                            form.balance.data):
                return redirect(url_for('users.sortedprofile', sortoption=0))
        return render_template('editbalance.html', title='Edit User Balance', form=form)

# make the edit password form
class EditPasswordForm(FlaskForm):
    password = PasswordField(_l('Old Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('New Password'), validators=[DataRequired()])
    password3 = PasswordField(
        _l('Repeat New Password'), validators=[DataRequired(),
                                           EqualTo('password2')])
    submit = SubmitField(_l('Update'))

# run the edit password form
@bp.route('/editpassword', methods=['GET', 'POST'])
def editpassword():
    if current_user.is_authenticated:
        form = EditPasswordForm()
        if form.validate_on_submit():
            user = User.get_by_auth(current_user.email, form.password.data)
            if user is None:
                print('Invalid password')
                return redirect(url_for('users.editpassword'))
            if User.edituser(current_user.id,
                            current_user.email,
                            form.password2.data,
                            current_user.firstname,
                            current_user.lastname,
                            current_user.address,
                            current_user.balance):
                return redirect(url_for('users.sortedprofile', sortoption=0))
        return render_template('editpassword.html', title='Edit User Password', form=form)