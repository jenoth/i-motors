from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from autocompany.orders.models import Order
from autocompany.orders.serializers import OrderSerializer


class OrderRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(auto_schema=None)
    def patch(self, request, *args, **kwargs):
        return super().patch(self, request, *args, **kwargs)


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
