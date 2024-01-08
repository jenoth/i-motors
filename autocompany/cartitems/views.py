import decimal

from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .models import CartItem as CartItemModel
from .serializers import CartItemsResponseSerializer, CartItemsRequestBodySerializer
from ..carts.models import Cart as CartModel
from ..products.models import Product as ProductModel
from ..utils.decorators import open_cart_validator


class CartItemCRUDView(generics.GenericAPIView):
    serializer_class = CartItemsResponseSerializer

    def get_open_cart_items(self, customer_id):
        """It will return tuple of cart_id and all products/items in a open/active cart of a customer.
        Customer can have only one open cart."""
        open_cart = CartModel.objects.get(customer=customer_id, status="OPEN")
        return open_cart.id, open_cart.cartitem_set.all()

    @open_cart_validator
    @swagger_auto_schema(responses={status.HTTP_200_OK: CartItemsResponseSerializer()})
    def get(self, request, customer_id):
        """Retrieve all products in the open cart of a customer."""
        return self._get_cart_items_response(customer_id)

    @open_cart_validator
    @swagger_auto_schema(
        request_body=CartItemsRequestBodySerializer(many=True),
        responses={status.HTTP_200_OK: CartItemsResponseSerializer()},
    )
    def post(self, request, customer_id):
        """Single API to handle all bulk insertion, updating and deletion of cart items"""
        # if existing products(db) are not in request data, DELETE all. removed product
        # if existing products(db) are available in request data, UPDATE all. existing product. to be updated
        # if products in request data which are not in existing(db) , CREATE all. non existing product. to be created

        # to have unique products with requested quantity
        requested_products_with_quantity = {data["id"]: data["quantity"] for data in request.data}

        cart_id, cart_items = self.get_open_cart_items(customer_id)
        existing_product_ids = set([item.product_id for item in cart_items])
        current_product_ids = set(requested_products_with_quantity)

        products_to_remove = existing_product_ids - current_product_ids
        products_to_insert = current_product_ids - existing_product_ids
        products_to_update = current_product_ids & existing_product_ids

        # Perform bulk deletion
        filter_condition = {"cart": cart_id, "product__in": products_to_remove}
        deleted_count, _ = CartItemModel.objects.filter(**filter_condition).delete()

        cart_object = CartModel.objects.get(pk=cart_id)
        objects_to_insert = [
            CartItemModel(cart=cart_object, product=ProductModel.objects.get(pk=k), quantity=v)
            for k, v in requested_products_with_quantity.items()
            if k in products_to_insert
        ]

        # Perform bulk insertion
        _ = CartItemModel.objects.bulk_create(objects_to_insert)

        # Perform bulk updating
        filter_condition = {"cart": cart_id, "product__in": products_to_update}
        products_to_bulk_update = CartItemModel.objects.filter(**filter_condition)

        for item in products_to_bulk_update:
            item.quantity = requested_products_with_quantity[item.product_id]
        CartItemModel.objects.bulk_update(products_to_bulk_update, ["quantity"])

        return self._get_cart_items_response(customer_id)

    def _get_cart_items_response(self, customer_id):
        # generating the response
        products_in_the_cart = []
        total_price_of_cart = decimal.Decimal()
        _, cart_items = self.get_open_cart_items(customer_id)
        for cart_item in cart_items:
            no_of_ordered_product = cart_item.quantity
            unit_price_of_ordered_product = cart_item.product.price
            total_price_of_ordered_product = unit_price_of_ordered_product * no_of_ordered_product
            products_in_the_cart.append(
                {
                    "id": cart_item.product.id,
                    "name": cart_item.product.name,
                    "unit_price": unit_price_of_ordered_product,
                    "quantity": no_of_ordered_product,
                    "total_price": total_price_of_ordered_product,
                }
            )
            total_price_of_cart += total_price_of_ordered_product

        return Response(
            CartItemsResponseSerializer(
                {
                    "cart_total": str(total_price_of_cart),
                    "products": products_in_the_cart,
                }
            ).data
        )

    def handle_exception(self, exc):
        if isinstance(exc, ValueError):
            error_response_data = {
                "type": "/errors/value-error",
                "title": "Value Error ",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "detail": str(exc),
                "instance": "trace_id",
            }
            return Response(data=error_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if isinstance(exc, ValidationError):
            error_response_data = {
                "type": "/errors/validation-error",
                "title": "Validation Error",
                "status": status.HTTP_400_BAD_REQUEST,
                "detail": str(exc),
                "instance": "trace_id",
            }
            return Response(data=error_response_data, status=status.HTTP_400_BAD_REQUEST)

        error_response_data = {
            "type": "/errors/common-exception",
            "title": "Unhandled Exception",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": str(exc),
            "instance": "trace_id",
        }
        return Response(data=error_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
