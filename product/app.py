from flask import Flask, redirect, render_template, request, make_response, session, abort, jsonify, url_for
import secrets
from functools import wraps
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import timedelta
import os
from dotenv import load_dotenv
import stripe

load_dotenv()



app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configure session cookie settings
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Adjust session expiration as needed
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Can be 'Strict', 'Lax', or 'None'


# Firebase Admin SDK setup
cred = credentials.Certificate("firebase-auth.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# Stripe setup

stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_key = stripe_secret_key


YOUR_DOMAIN = 'http://localhost:5000'

########################################
""" Authentication and Authorization """

# Decorator for routes that require authentication
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if 'user' not in session:
            return redirect(url_for('login'))
        
        else:
            return f(*args, **kwargs)
        
    return decorated_function


@app.route('/auth', methods=['POST'])
def authorize():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return "Unauthorized", 401

    token = token[7:]  # Strip off 'Bearer ' to get the actual token

    try:
        decoded_token = auth.verify_id_token(token, check_revoked=True, clock_skew_seconds=60) # Validate token here
        session['user'] = decoded_token # Add user to session
        return redirect(url_for('dashboard'))
    
    except:
        return "Unauthorized", 401


#####################
""" Public Routes """

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')

@app.route('/signup')
def signup():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('signup.html')


@app.route('/reset-password')
def reset_password():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('forgot_password.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove the user from session
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session', '', expires=0)  # Optionally clear the session cookie
    return response

@app.route('/products')
def products():
    # Get all products from Firestore
    products_ref = db.collection('products')
    products = products_ref.stream()

    # Convert Firestore results to a list and include the document ID
    product_list = []
    for product in products:
        product_data = product.to_dict()
        product_data['id'] = product.id  # Add the Firestore document ID to the product data
        product_list.append(product_data)

    return render_template('products.html', products=product_list)


@app.route('/product/<product_id>')
def product_detail(product_id):
    # Get the specific product from Firestore using the product_id
    product_ref = db.collection('products').document(product_id)
    product = product_ref.get()

    if not product.exists:
        return "Product not found", 404

    product_data = product.to_dict()
    product_data['id'] = product.id  # Store the Firestore document ID as 'id'

    # Return the product data to the template for rendering
    return render_template('product_detail.html', product=product_data)

'''@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
'''

##############################################
""" Private Routes (Require authorization) """

@app.route('/dashboard')
@auth_required
def dashboard():

    return render_template('dashboard.html')

@app.route('/create-checkout-session', methods=['GET', 'POST'])
@auth_required
def create_checkout_session():

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price' : "price_1QvA4iBZTAUNX1U8pYpvMm1F",
                    'quantity': 1,
                }
            ],
            mode = 'subscription',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )

    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, 303)

@app.route('/success')
@auth_required
def payment_success():
    session.pop('cart', None)  # Clear the cart
    return render_template('success.html')

@app.route('/cancel')
@auth_required
def payment_cancel():
    return render_template('cancel.html')


@app.route('/add-product', methods=['GET', 'POST'])
@auth_required
def add_product():
    if request.method == 'POST':
        # Get the data from the form
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])  # Convert price to a float
        image_url = request.form['image_url']
        category = request.form['category']

        # Add the product data to Firestore
        products_ref = db.collection('products')
        product_data = {
            'name': name,
            'description': description,
            'price': price,
            'image_url': image_url,
            'category': category,
        }
        products_ref.add(product_data)

        return redirect(url_for('admin_dashboard'))  # Change 'admin_dashboard' to the route for your admin panel

    return render_template('add_product.html')  # Render the form when GET request


@app.route('/admin-dashboard')
def admin_dashboard():
    try:
        # Fetch all products from Firestore
        products_ref = db.collection('products')
        products = products_ref.stream()
        product_list = []
        for product in products:
            product_dict = product.to_dict()
            product_dict['id'] = product.id  # Add the product ID to the data
            product_list.append(product_dict)

        return render_template('admin_dashboard.html', products=product_list)
    except Exception as e:
        flash(f"Error fetching products: {e}", "error")
        return render_template('admin_dashboard.html', products=[])


@app.route('/cart')
@auth_required
def cart():
    # Retrieve cart from session
    cart_items = session.get('cart', [])
    
    # Calculate total price
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/add-to-cart/<product_id>')
@auth_required
def add_to_cart(product_id):
    # Get product data from Firestore
    product_ref = db.collection('products').document(product_id)
    product = product_ref.get()

    if not product.exists:
        return "Product not found", 404

    product_data = product.to_dict()

    # Retrieve the current cart from the session
    cart = session.get('cart', [])

    # Check if the product is already in the cart
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            break
    else:
        # If the product isn't in the cart, add it
        cart.append({
            'id': product_id,
            'name': product_data['name'],
            'price': product_data['price'],
            'image_url': product_data['image_url'],
            'quantity': 1
        })

    # Save the updated cart back to the session
    session['cart'] = cart

    return redirect(url_for('cart'))  # Redirect to the cart page

@app.route('/remove-from-cart/<product_id>')
@auth_required
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    
    # Save the updated cart to session
    session['cart'] = cart

    return redirect(url_for('cart'))

@app.route('/checkout')
@auth_required
def checkout():
    cart_items = session.get('cart', [])
    
    # Calculate total price
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)

@app.route('/edit-product/<product_id>', methods=['GET', 'POST'])
@auth_required
def edit_product(product_id):
    try:
        # Fetch the product from Firestore
        product_ref = db.collection('products').document(product_id)
        product = product_ref.get()

        # Check if product exists
        if not product.exists:
            flash("Product not found", "error")
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard if product is not found

        product_data = product.to_dict()

        if request.method == 'POST':
            # Get data from the form
            name = request.form.get('name')
            description = request.form.get('description')
            price = request.form.get('price')
            image_url = request.form.get('image_url')
            category = request.form.get('category')

            # Validate price
            try:
                price = float(price)  # Convert price to float
                if price <= 0:
                    flash("Price must be a positive number", "error")
                    return render_template('edit_product.html', product=product_data)
            except ValueError:
                flash("Invalid price. Please enter a valid number", "error")
                return render_template('edit_product.html', product=product_data)

            # Update the product data in Firestore
            product_data = {
                'name': name,
                'description': description,
                'price': price,
                'image_url': image_url,
                'category': category,
            }

            product_ref.update(product_data)
            flash("Product updated successfully", "success")
            return redirect(url_for('admin_dashboard'))  # Redirect to the admin dashboard after editing

        # Display the edit form pre-filled with current product data
        return render_template('edit_product.html', product=product_data, product_id=product_id)

    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for('admin_dashboard'))

@app.route('/delete-product/<product_id>', methods=['GET','POST'])
@auth_required
def delete_product(product_id):
    # Fetch the product from Firestore
    product_ref = db.collection('products').document(product_id)
    product = product_ref.get() 

    if not product.exists:
        return "Product not found", 404

    # Delete the product from Firestore
    product_ref.delete()

    return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard after deletion

if __name__ == '__main__':
    app.run(debug=True)