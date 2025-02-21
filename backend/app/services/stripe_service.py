from flask import current_app
import stripe

stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

def create_payment_intent(amount, currency='usd'):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
        )
        return payment_intent
    except Exception as e:
        return str(e)

def confirm_payment_intent(payment_intent_id, payment_method_id):
    try:
        payment_intent = stripe.PaymentIntent.confirm(
            payment_intent_id,
            payment_method=payment_method_id,
        )
        return payment_intent
    except Exception as e:
        return str(e)

def retrieve_payment_intent(payment_intent_id):
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return payment_intent
    except Exception as e:
        return str(e)