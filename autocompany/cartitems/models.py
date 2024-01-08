from django.core.exceptions import ValidationError
from django.db import models

from autocompany.products.models import Product


def validate_positive(value):
    if value < 1:
        raise ValidationError(f"{value} is not a positive number")


class CartItem(models.Model):
    """It can be considered as OrderedItem model as well. Joining / Intermediate table of cart and products(ordered items)
    which are in Many-to-Many relationship."""

    cart = models.ForeignKey("carts.Cart", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[validate_positive])

    class Meta:
        db_table = "cart_item"
        db_table_comment = "Ordered(cart) items of customer"
        unique_together = (
            "cart",
            "product",
        )
