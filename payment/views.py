import stripe
from django.http import JsonResponse
from django.views import View
from rest_framework import viewsets, status, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from borrowing.models import Borrowing
from library_service import settings
from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentDetailSerializer



class PaymentViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if not user.is_staff:
            return queryset.filter(borrowing__user=user)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentSerializer
        return PaymentDetailSerializer


class PaymentSuccessView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        session_id = request.query_params.get("session_id")
        session = stripe.checkout.Session.retrieve(session_id)
        payment = Payment.objects.get(session_id=session_id)

        if session.get("payment_status") == "paid":
            payment.status = Payment.Status.PAID
            payment.save()

            return Response({"detail": "Payment succeeded!"})


class PaymentCancelView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        return Response(
            {
                "detail": "Your payment session is still "
                "available for 24 hours. Please complete your "
                "payment within this period."
            }
        )