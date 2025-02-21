from flask import jsonify, request
from app.services.firebase_service import get_user_data
from app.services.stripe_service import create_payment_intent
from app.services.eco_points_service import earn_eco_points
from app.models import Product

class MarketplaceController:
    def get_products(self):
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200

    def get_product(self, product_id):
        product = Product.query.get(product_id)
        if product:
            return jsonify(product.to_dict()), 200
        return jsonify({"error": "Product not found"}), 404

    def purchase_product(self):
        data = request.json
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        payment_method_id = data.get('payment_method_id')

        user_data = get_user_data(user_id)
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        payment_intent = create_payment_intent(payment_method_id, product.price)

        if payment_intent['status'] == 'succeeded':
            earn_eco_points(user_id, product.eco_points)
            return jsonify({"message": "Purchase successful", "eco_points": product.eco_points}), 200

        return jsonify({"error": "Payment failed"}), 400