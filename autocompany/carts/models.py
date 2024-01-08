from django.db import models

from autocompany.cartitems.models import CartItem
from autocompany.customers.models import Customer
from autocompany.products.models import Product


class Cart(models.Model):
    """It is a temporary storage of an ordering process. This records should be removed or marked as non-active once the
    customer finishes his order or if he or she ends the session or logout."""

    # OPEN: Active cart of the customer. One customer can have only one OPEN cart.
    # SUBMITTED: Cart is submitted and initiated the order. It is Inactive cart.
    CartStatus = models.TextChoices("CartStatus", "OPEN SUBMITTED")

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cartitems = models.ManyToManyField(Product, through=CartItem, through_fields=("cart", "product"))
    status = models.CharField(choices=CartStatus.choices, max_length=10, default=CartStatus.OPEN)

    class Meta:
        db_table = "cart"

    def __str__(self):
        return f"{self.id}, Shopping cart of {self.customer}"

    def save(self, *args, **kwargs):
        """Overriding the existing save method which is triggered when create or update the record."""

        open_cart = Cart.objects.filter(customer=self.customer, status=self.CartStatus.OPEN)
        if self.pk is None:
            if self.status == self.CartStatus.SUBMITTED:
                raise ValueError("Customer cannot create a cart with status, SUBMITTED")

            if open_cart.count() > 0:
                raise ValueError("Customer already has open cart which is a db integrity error according to our design")
        else:
            if self.status == self.CartStatus.OPEN:
                raise ValueError("Customer cannot update a cart with status, OPEN")

        super().save(*args, **kwargs)
