from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from payment.views import PaymentViewSet, PaymentSuccessView, PaymentCancelView

app_name = "payments"

router = routers.DefaultRouter()
router.register("payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "success/",
        PaymentSuccessView.as_view(),
        name="payment-success"
    ),
    path(
        "cancel/",
        PaymentCancelView.as_view(),
        name="payment-cancel"
    ),
]