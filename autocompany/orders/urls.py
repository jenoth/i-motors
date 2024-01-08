from django.urls import path

from autocompany.orders.views import OrderRetrieveUpdateView, OrderListView

urlpatterns = [
    path("", OrderListView.as_view(), name="list-orders"),
    path("<int:pk>/", OrderRetrieveUpdateView.as_view(), name="order-retrieve-update-delete"),
]
