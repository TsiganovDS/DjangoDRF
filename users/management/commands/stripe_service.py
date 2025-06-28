import os

import stripe
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_product(name):
    """Создание продукта"""
    product = stripe.Product.create(
        name=name,
    )
    return product.id


def create_price(product_id, amount, currency="rub"):
    """Создает цену в stripe"""
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),
        currency=currency,
    )
    return price.id


def create_checkout_session(price_id):
    """Создает ссесию на оплату в stripe"""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="lms:success",
        cancel_url="lms:cancel",
    )
    return session.get("id"), session.get("url")
