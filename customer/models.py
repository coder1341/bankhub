from django.db import models
from django.contrib.auth.models import User
import random


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    account_number = models.CharField(max_length=10, unique=True, blank=True)

    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    phone_number = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)

    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    account_type = models.CharField(
        max_length=50,
        default="Savings"
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = str(
                random.randint(1000000000, 9999999999)
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE
    )

    transaction_type = models.CharField(
        max_length=20
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.transaction_type} - ${self.amount}"