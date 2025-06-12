import stripe
import os

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "sk_test_...")
stripe.api_key = STRIPE_API_KEY

def create_stripe_checkout_session(amount, currency, success_url, cancel_url, metadata=None):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": currency,
                "unit_amount": int(amount * 100),
                "product_data": {"name": "Online Cinema order"},
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata=metadata or {},
    )
    return session
