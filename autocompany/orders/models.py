from django.db import models

from autocompany.carts.models import Cart


class Order(models.Model):
    # INITIATED: submitted the basket, CONFIRMED: Entered shipping details and payment related stuffs
    # SHIPPED: shipped(delivered) to the customer, CANCELLED: cancelled the order by either customer or business
    OrderStatus = models.TextChoices("OrderStatus", "INITIATED CONFIRMED SHIPPED CANCELLED")

    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    delivery_date = models.DateTimeField(null=True)
    status = models.CharField(choices=OrderStatus.choices, max_length=10, default=OrderStatus.INITIATED)
    # This address is only used for this order. Otherwise, we can use the default address of the user.
    shipping_address = models.TextField(null=True, blank=True)
    # Any additional details can be stored here. Eg, any reason for order cancellation.
    comments = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "order"
        db_table_comment = "Orders of customer"
