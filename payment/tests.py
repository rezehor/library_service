import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from borrowing.tests import sample_borrowing
from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentDetailSerializer

PAYMENT_URL = reverse("payments:payments-list")


def sample_payment(**params) -> Payment:
    defaults = {
        "status": "Paid",
        "type": "Payment",
        "session_url": "https://example.com",
        "session_id": str(uuid.uuid4()),
        "money_to_pay": 20.00,
    }
    defaults.update(params)
    return Payment.objects.create(**defaults)


def detail_url(payment_id):
    return reverse("payments:payments-detail", args=[payment_id])


class UnauthenticatedPaymentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PAYMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPaymentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            email="user1@test.test", password="testpassword"
        )
        self.user2 = get_user_model().objects.create_user(
            email="user2@test.test", password="testpassword"
        )
        self.borrowing1 = sample_borrowing(user=self.user1)
        self.borrowing2 = sample_borrowing(user=self.user2)
        self.payment1 = sample_payment(borrowing=self.borrowing1)
        self.payment2 = sample_payment(borrowing=self.borrowing2)
        self.client.force_authenticate(self.user1)

    def test_create_payment(self):
        borrowing = sample_borrowing(user=self.user1)
        payload = {
            "status": "Pending",
            "type_field": "Payment",
            "borrowing": borrowing.id,
            "session_url": "https://example.com",
            "session_id": "session_id",
            "money_to_pay": 15.00,
        }
        res = self.client.post(PAYMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_payment_detail(self):
        borrowing = sample_borrowing(user=self.user1)
        payment = sample_payment(borrowing_id=borrowing.id)
        url = detail_url(payment.id)
        res = self.client.get(url)
        serializer = PaymentDetailSerializer(payment)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_user_cannot_see_others_payments(self):
        self.client.force_login(self.user1)
        res = self.client.get(PAYMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)


class AdminBorrowingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="admin@admin.test", password="testpassword", is_staff=True,
        )
        self.user = get_user_model().objects.create_user(
            email="user@test.test", password="testpassword"
        )

        self.borrowing = sample_borrowing(user=self.user)
        self.payment = sample_payment(borrowing=self.borrowing)
        self.client.force_authenticate(self.admin)

    def test_admin_can_see_all_payments(self):
        res = self.client.get(PAYMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
