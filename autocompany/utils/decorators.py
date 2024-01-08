from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from autocompany.carts.models import Cart


def open_cart_validator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if Cart.objects.filter(customer=kwargs["customer_id"], status="OPEN").exists():
            return func(*args, **kwargs)

        error_response_data = {
            "type": "/errors/no-open-cart-available-for-a-customer",
            "title": "No open cart for a customer",
            "status": status.HTTP_404_NOT_FOUND,
            "detail": "There is not a open cart for the customer",
            "instance": "trace_id",
        }
        return Response(data=error_response_data, status=status.HTTP_404_NOT_FOUND)

    return wrapper
