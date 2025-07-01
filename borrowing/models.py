from django.db import models

from book.models import Book
from library_service.settings import AUTH_USER_MODEL


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-expected_return_date"]

    def __str__(self):
        return f"User({self.user.id}), Book({self.book.id}), Date({self.borrow_date}-{self.expected_return_date})"
