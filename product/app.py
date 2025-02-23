from flask import Flask, redirect, render_template, request, make_response, session, abort, jsonify, url_for, flash 
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
        
        # Check if user has the required role (e.g., admin)
        user_role = session.get('role', 'user')  # Default to 'user' if no role found
        if f.__name__ in ['admin_dashboard', 'add_product', 'edit_product', 'delete_product'] and user_role != 'admin':
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for('dashboard'))  # Or you could show an access denied page
        
        return f(*args, **kwargs)
    
    return decorated_function



@app.route('/auth', methods=['POST'])
def authorize():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return "Unauthorized", 401

    token = token[7:]  # Strip off 'Bearer ' to get the actual token

    try:
        decoded_token = auth.verify_id_token(token, check_revoked=True, clock_skew_seconds=60)  # Validate token
        session['user'] = decoded_token  # Store the decoded token in the session
        
        user_id = decoded_token['uid']  # Get the Firebase UID

        # Check Firestore for the user's role
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        # If user does not exist, set default role
        if not user_doc.exists:
            user_ref.set({
                'email': decoded_token['email'],
                'role': 'user'  # Default role as 'user'
            })
            session['role'] = 'user'  # Default to 'user' if no role set
        else:
            user_data = user_doc.to_dict()
            session['role'] = user_data.get('role', 'user')  # Assign role from Firestore

        return redirect(url_for('dashboard'))  # Redirect to the dashboard

    except Exception as e:
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
    session.pop('role', None)  # Remove role from session
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session', '', expires=0)  # Optionally clear the session cookie
    return response

@app.route('/about')
def about():
    return render_template('about.html')

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
    user = session.get('user', {})
    user_id = user.get('uid')
    
    # Fetch user data from Firestore
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    
    if user_doc.exists:
        user_data = user_doc.to_dict()
    else:
        user_data = {}
    
    # Fetch user's orders from Firestore without ordering
    orders_ref = db.collection('orders').where('user_id', '==', user_id)
    orders = orders_ref.stream()

    # Convert to list, and then sort by timestamp manually
    order_list = [order.to_dict() for order in orders]
    order_list.sort(key=lambda x: x['timestamp'], reverse=True)  # Sort by timestamp in descending order

    # Limit to the most recent 3 orders (you can adjust the limit)
    recent_orders = order_list[:3]
    
    return render_template('dashboard.html', user=user_data, recent_orders=recent_orders)

    user = session.get('user', {})
    user_id = user.get('uid')
    
    # Fetch user data from Firestore
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    
    if user_doc.exists:
        user_data = user_doc.to_dict()
    else:
        user_data = {}
    
    # Fetch the user's orders from Firestore (optional: show recent orders)
    orders_ref = db.collection('orders').where('user_id', '==', user_id).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(3)
    orders = orders_ref.stream()
    
    order_list = []
    for order in orders:
        order_data = order.to_dict()
        order_data['id'] = order.id
        order_list.append(order_data)
    
    return render_template('dashboard.html', user=user_data, recent_orders=order_list)

@app.route('/profile')
@auth_required
def profile():
    user = session.get('user', {})
    user_id = user.get('uid')
    
    # Fetch user data from Firestore
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    
    if user_doc.exists:
        user_data = user_doc.to_dict()
    else:
        user_data = {}
    
    return render_template('profile.html', user=user_data)

@app.route('/update-profile', methods=['GET', 'POST'])
@auth_required
def update_profile():
    user = session.get('user', {})
    user_id = user.get('uid')
    
    # Fetch user data from Firestore
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    
    if user_doc.exists:
        user_data = user_doc.to_dict()
    else:
        user_data = {}
    
    if request.method == 'POST':
        # Handle form submission to update the profile
        username = request.form.get('username')
        dob = request.form.get('dob')
        location = request.form.get('location')
        
        # Update Firestore with the new information
        user_ref.update({
            'username': username,
            'dob': dob,
            'location': location,
        })
        
        # Update session with the new data (optional, if you want session to reflect the changes immediately)
        session['user']['username'] = username
        session['user']['dob'] = dob
        session['user']['location'] = location
        
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))  # Redirect to the profile page after updating
    
    # If it's a GET request, render the profile update form with the current user data
    return render_template('update_profile.html', user=user_data)

@app.route('/order-history')
@auth_required
def order_history():
    user_id = session['user']['uid']  # Get the authenticated user's ID

    # Fetch the user's orders from Firestore without ordering
    orders_ref = db.collection('orders').where('user_id', '==', user_id)
    orders = orders_ref.stream()

    # Convert Firestore results to a list of dictionaries
    order_list = []
    for order in orders:
        order_data = order.to_dict()
        order_data['id'] = order.id  # Add Firestore document ID
        order_list.append(order_data)

    return render_template('order_history.html', orders=order_list)

@app.route('/order/<order_id>')
@auth_required
def order_detail(order_id):
    user_id = session['user']['uid']  # Get the authenticated user's ID
    
    # Fetch the order from Firestore
    order_ref = db.collection('orders').document(order_id)
    order = order_ref.get()

    if not order.exists:
        return "Order not found", 404

    order_data = order.to_dict()
    
    # Ensure the order belongs to the logged-in user
    if order_data['user_id'] != user_id:
        return "Unauthorized", 403

    return render_template('order_detail.html', order=order_data)

@app.route('/create-checkout-session', methods=['GET', 'POST'])
@auth_required
def create_checkout_session():
    try:
        # Retrieve the cart from session
        cart_items = session.get('cart', [])
        
        # Prepare the line_items for Stripe (dynamically based on cart content)
        line_items = []
        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['name'],
                    },
                    'unit_amount': int(item['price'] * 100),  # Stripe requires amount in cents
                },
                'quantity': item['quantity'],
            })

        # Create the Checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )

        return redirect(checkout_session.url, 303)

    except Exception as e:
        return str(e)

@app.route('/success')
@auth_required
def payment_success():
    # Retrieve cart data from the session
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    # Get the user ID from the session
    user_id = session['user']['uid']

    # Save the order to Firestore
    order_ref = db.collection('orders').add({
        'user_id': user_id,
        'items': cart_items,
        'total_price': total_price,
        'status': 'completed',  # Mark order as completed
        'timestamp': firestore.SERVER_TIMESTAMP  # Timestamp for sorting
    })

    # Clear the cart after successful payment
    session.pop('cart', None)
    
    flash("Payment successful! Your order has been placed.", "success")
    
    # Render the success page with cart items and total price
    return render_template('success.html', cart_items=cart_items, total_price=total_price)

@app.route('/cancel')
@auth_required
def payment_cancel():
    flash("Payment was canceled. Please try again.", "error")
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
    if session.get('role') != 'admin':
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('dashboard')) 

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

@app.route('/checkout', methods=['GET', 'POST'])
@auth_required
def checkout():
    if request.method == 'GET':
        # Display the checkout page with cart items and total price
        cart_items = session.get('cart', [])
        
        # Calculate total price
        total_price = sum(item['price'] * item['quantity'] for item in cart_items)

        return render_template('checkout.html', cart_items=cart_items, total_price=total_price)
    
    elif request.method == 'POST':
        # Redirect to create checkout session when user submits the checkout form
        return redirect(url_for('create_checkout_session'))  # This will trigger the create-checkout-session route

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