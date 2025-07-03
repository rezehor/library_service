from django.db import models


class Book(models.Model):
    class Cover(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(choices=Cover, max_length=10)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title
