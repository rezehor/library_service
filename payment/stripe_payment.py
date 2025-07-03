import stripe
import os
from rest_framework.reverse import reverse

from borrowing.models import Borrowing
from library_service import settings
from payment.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_checkout_session(payment, request):
    success_url = request.build_absolute_uri(
        reverse("payments:payment-success")
    ) + "?session_id={CHECKOUT_SESSION_ID}"

    cancel_url = request.build_absolute_uri(
        reverse("payments:payment-cancel")
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": int(payment.money_to_pay * 100),
                "product_data": {
                    "name": f"Fine for {payment.borrowing.book.title}",
                },
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"payment_id": payment.id}
    )
    return session
