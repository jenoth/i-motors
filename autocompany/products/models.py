import uuid

from django.db import models


class Product(models.Model):
    # sku, stock keeping unit can be used to uniquely identify a product later. Also, we can use ULID instead of UUID.
    sku = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=1000)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.name
