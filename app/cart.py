from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user
from flask import Blueprint
import psycopg2
import psycopg2.extras

bp = Blueprint('cart', __name__)

# @bp.route('/cart')
# def cart():
#     return render_template('cart.html', title='Cart')

DB_HOST = "localhost"
DB_NAME = "amazon"
DB_USER = "edgardy17"
DB_PASS = "dbpasswd"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 
@bp.route('/cart')
def carts():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    cursor.execute("SELECT * FROM PRODUCTS")
    rows = cursor.fetchall()
    return render_template('cart.html', products=rows)

# @bp.route('/cart/add', methods=['POST'])
# def add_product_to_cart():
#     _quantity = int(request.form['quantity'])
#     _code = request.form['code']
#     # validate the received values
#     if _quantity and _code and request.method == 'POST':
 
#         cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
#         cursor.execute('SELECT * FROM product WHERE code = %s', (_code,))
#         row = cursor.fetchone()
                 
#         itemArray = { row['code'] : {'name' : row['name'], 'code' : row['code'], 'quantity' : _quantity, 'price' : row['price'], 'total_price': _quantity * row['price']}}
                 
#         all_total_price = 0
#         all_total_quantity = 0
                 
#         session.modified = True
#         if 'cart_item' in session:
#             if row['code'] in session['cart_item']:
#                 for key, value in session['cart_item'].items():
#                     if row['code'] == key:
#                         old_quantity = session['cart_item'][key]['quantity']
#                         total_quantity = old_quantity + _quantity
#                         session['cart_item'][key]['quantity'] = total_quantity
#                         session['cart_item'][key]['total_price'] = total_quantity * row['price']
#             else:
#                 session['cart_item'] = array_merge(session['cart_item'], itemArray)
         
#             for key, value in session['cart_item'].items():
#                 individual_quantity = int(session['cart_item'][key]['quantity'])
#                 individual_price = float(session['cart_item'][key]['total_price'])
#                 all_total_quantity = all_total_quantity + individual_quantity
#                 all_total_price = all_total_price + individual_price
#         else:
#             session['cart_item'] = itemArray
#             all_total_quantity = all_total_quantity + _quantity
#             all_total_price = all_total_price + _quantity * row['price']
             
#         session['all_total_quantity'] = all_total_quantity
#         session['all_total_price'] = all_total_price
                 
#         return render_template('cart.html', products=rows)
#     else:
#         return 'Error while adding item to cart'
 
# @bp.route('/cart/empty')
# def empty_cart():
#     try:
#         session.clear()
#         return redirect(url_for('.cart'))
#     except Exception as e:
#         print(e)
 
# @bp.route('/cart/delete/<string:code>')
# def delete_product(code):
#     try:
#         all_total_price = 0
#         all_total_quantity = 0
#         session.modified = True
         
#         for item in session['cart_item'].items():
#             if item[0] == code:    
#                 session['cart_item'].pop(item[0], None)
#                 if 'cart_item' in session:
#                     for key, value in session['cart_item'].items():
#                         individual_quantity = int(session['cart_item'][key]['quantity'])
#                         individual_price = float(session['cart_item'][key]['total_price'])
#                         all_total_quantity = all_total_quantity + individual_quantity
#                         all_total_price = all_total_price + individual_price
#                 break
         
#         if all_total_quantity == 0:
#             session.clear()
#         else:
#             session['all_total_quantity'] = all_total_quantity
#             session['all_total_price'] = all_total_price
             
#         return redirect(url_for('.cart'))
#     except Exception as e:
#         print(e)
 
# def array_merge( first_array , second_array ):
#     if isinstance( first_array , list ) and isinstance( second_array , list ):
#         return first_array + second_array
#     elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
#         return dict( list( first_array.items() ) + list( second_array.items() ) )
#     elif isinstance( first_array , set ) and isinstance( second_array , set ):
#         return first_array.union( second_array )
#     return False
 
# if __name__ == "__main__":
#     app.run(debug=True)