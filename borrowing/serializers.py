from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from book.serializers import BookSerializer
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date", "actual_return_date", "book")

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


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "actual_return_date")

    def validate(self, data):
        if self.instance.actual_return_date:
            raise serializers.ValidationError("Borrowing has already been returned.")
        return data

    def update(self, instance, validated_data):
        instance.actual_return_date = datetime.now().date()
        instance.save()
        instance.book.inventory += 1
        instance.book.save(update_fields=["inventory"])
        return instance
