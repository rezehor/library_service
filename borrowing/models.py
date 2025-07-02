from django.db import models
from rest_framework.exceptions import ValidationError

from book.models import Book
from library_service.settings import AUTH_USER_MODEL


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-expected_return_date"]

    def __str__(self):
        return f"User({self.user.id}), Book({self.book.id}), Date({self.borrow_date}-{self.expected_return_date})"


    @staticmethod
    def validate_borrowing(
            borrow_date,
            expected_return_date,
            actual_return_date,
            book,
            error_to_raise,
    ):
        if expected_return_date < borrow_date:
            raise error_to_raise({
                "expected_return_date": f"Expected return date {expected_return_date} cannot be before borrow date {borrow_date}."
            })

        if actual_return_date and actual_return_date < borrow_date:
            raise error_to_raise({
                "actual_return_date": f"Actual return date {actual_return_date} cannot be before borrow date {borrow_date}."
            })

        if book.inventory <= 0:
            raise error_to_raise({
                "book": "Unfortunately, this book is no longer available."
            })


    def clean(self):
        self.validate_borrowing(
            self.borrow_date,
            self.expected_return_date,
            self.actual_return_date,
            self.book,
            ValidationError
        )

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )