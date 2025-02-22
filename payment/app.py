#flask payment with stripe

from flask import Flask, redirect, request
import stripe

app = Flask(__name__, static_url_path='', static_folder='static')

YOUR_DOMAIN = 'http://localhost:5000'

stripe.api_key = "sk_test_51Qv9QoBZTAUNX1U8J7EIDCIj8ENtJUslAvdgc3FswWjSf5BRkOyIQ0159zp9cJ1ihAx8mhUAWD80IsDLokvCWPXP00JGWokq2k"

@app.route('/create-checkout-session', methods=['POST'])
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
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )

    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, 303)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
