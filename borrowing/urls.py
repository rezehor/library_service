from django.urls import path, include
from rest_framework.routers import DefaultRouter
from borrowing.views import BorrowingViewSet

app_name = "borrowing"

router = DefaultRouter()

router.register("borrowings", BorrowingViewSet, basename="borrowings")

urlpatterns = [
    path("", include(router.urls)),
]