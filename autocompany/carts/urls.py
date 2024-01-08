from django.urls import path

from .views import CartListCreateView, CartDeleteView

urlpatterns = [
    path("", CartListCreateView.as_view(), name="cart-list-create"),
    path("<int:pk>/", CartDeleteView.as_view(), name="cart-delete"),
]
