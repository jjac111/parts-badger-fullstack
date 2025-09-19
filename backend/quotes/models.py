from django.db import models


class Part(models.Model):
    stock_code = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.stock_code}"


class Quote(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )
    name = models.CharField(max_length=128)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name}"


class QuoteLineItem(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="items")
    part = models.ForeignKey(Part, on_delete=models.PROTECT, related_name="line_items")
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class CsvResult(models.Model):
    stock_code = models.CharField(max_length=100, db_index=True)
    number_quotes_found = models.IntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    file_uploaded = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
