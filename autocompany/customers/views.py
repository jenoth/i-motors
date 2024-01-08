from typing import Literal

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializer, CustomerCartSubmitSerializer
from ..carts.models import Cart as CartModel
from ..carts.serializers import CustomerCartSerializer
from ..orders.models import Order
from ..utils.decorators import open_cart_validator

cart_status_query_param = openapi.Parameter(
    name="cart_status",
    in_=openapi.IN_QUERY,
    required=False,
    type=openapi.TYPE_STRING,
    enum=["OPEN", "SUBMITTED"],
    description="Status of a cart like, OPEN or SUBMITTED",
)


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @swagger_auto_schema(auto_schema=None)
    def patch(self, request, *args, **kwargs):
        return super().patch(self, request, *args, **kwargs)


class CustomerCartListView(generics.GenericAPIView):
    serializer_class = CustomerCartSerializer

    def get_cart_queryset(self, customer_id, cart_status: Literal["OPEN", "SUBMITTED"]):
        return CartModel.objects.filter(
            customer=customer_id, status__in=(cart_status,) if cart_status else ("OPEN", "SUBMITTED")
        )

    @swagger_auto_schema(manual_parameters=[cart_status_query_param])
    def get(self, request, customer_id):
        """Retrieve all carts of a customer with or without status filtered."""
        queryset = self.get_cart_queryset(customer_id, request.query_params.get("cart_status"))
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)


class CustomerCartSubmitView(generics.GenericAPIView):
    serializer_class = CustomerCartSubmitSerializer

    @open_cart_validator
    def patch(self, request, customer_id):
        """Submit a open cart of a customer to initiate the order."""
        cart = CartModel.objects.get(customer=customer_id, status="OPEN")
        cart.status = "SUBMITTED"
        cart.save()

        order = Order.objects.create(cart=cart)

        serializer = self.serializer_class(
            {"order_id": order.id, "detail": "Cart has been submitted and order has been placed."}
        )
        return Response(serializer.data)
