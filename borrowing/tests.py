from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from book.tests import sample_book
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingDetailSerializer

BORROWING_URL = reverse("borrowings:borrowings-list")


def sample_borrowing(**params) -> Borrowing:
    book = sample_book()
    defaults = {
        "borrow_date": "2025-07-03",
        "expected_return_date": "2025-08-03",
        "actual_return_date": None,
        "book": book,
        "user": params.get("user")
    }
    defaults.update(params)
    return Borrowing.objects.create(**defaults)


def detail_url(borrowing_id):
    return reverse("borrowings:borrowings-detail", args=[borrowing_id])


class UnauthenticatedBorrowingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingAPITests(TestCase):
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
        self.client.force_authenticate(self.user1)

    def test_create_borrowing(self):
        book = sample_book()
        payload = {
            "borrow_date": "2025-07-03",
            "expected_return_date": "2025-08-03",
            "book": book.id,
        }
        res = self.client.post(BORROWING_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieve_borrowing_detail(self):
        borrowing = sample_borrowing(user=self.user1)
        url = detail_url(borrowing.id)
        res = self.client.get(url)
        serializer = BorrowingDetailSerializer(borrowing)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_user_cannot_see_others_borrowings(self):
        self.client.force_login(self.user1)
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        for item in res.data:
            borrowing = Borrowing.objects.get(id=item["id"])
            self.assertEqual(borrowing.user, self.user1)


class AdminBorrowingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="admin@admin.test", password="testpassword", is_staff=True,
        )
        self.user = get_user_model().objects.create_user(
            email="user@test.test", password="testpassword"
        )

        self.borrowing1 = sample_borrowing(user=self.user)
        self.borrowing2 = sample_borrowing(
            user=self.user, actual_return_date="2025-08-03"
        )
        self.client.force_authenticate(self.admin)

    def test_admin_user_sees_all_borrowings(self):
        self.client.force_login(self.admin)
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)


