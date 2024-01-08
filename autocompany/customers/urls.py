from django.urls import path

from .views import CustomerListCreateView, CustomerDetailView, CustomerCartListView, CustomerCartSubmitView

urlpatterns = [
    path("", CustomerListCreateView.as_view(), name="customer-list-create"),
    path("<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
    path("<int:customer_id>/carts/", CustomerCartListView.as_view(), name="customer-cart-list"),
    path("<int:customer_id>/carts/submit/", CustomerCartSubmitView.as_view(), name="customer-cart-submit"),
]
