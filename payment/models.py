from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending"
        PAID = "Paid"

    class Type(models.TextChoices):
        PAYMENT = "Payment"
        FINE = "Fine"

    status = models.CharField(choices=Status, max_length=10, default=Status.PENDING)
    type = models.CharField(choices=Type, max_length=10)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField(null=True, blank=True)
    session_id = models.CharField(max_length=64, unique=True, null=True, blank=True)
    money_to_pay = models.DecimalField(decimal_places=2, max_digits=7)

    def __str__(self):
        return self.session_id
