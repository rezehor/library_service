from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book.serializers import BookSerializer
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date", "actual_return_date", "book", "user")

    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs=attrs)
        Borrowing.validate_borrowing(
            attrs["borrow_date"],
            attrs["expected_return_date"],
            attrs["actual_return_date"],
            attrs["book"],
            ValidationError
        )
        return data


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(read_only=True)
