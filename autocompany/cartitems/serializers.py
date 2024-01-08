from rest_framework import serializers

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class CartItemsProductsSerializer(serializers.Serializer):
    """It represents ordered item which is product"""

    id = serializers.IntegerField()
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class CartItemsResponseSerializer(serializers.Serializer):
    """Complete set of fields of a success response"""

    products = CartItemsProductsSerializer(many=True, read_only=True)
    cart_total = serializers.DecimalField(max_digits=10, decimal_places=2)


class CartItemsRequestBodySerializer(serializers.Serializer):
    """It represents the request payload of product and the quantity of a cart"""

    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
