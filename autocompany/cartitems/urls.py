from django.urls import path

from .views import CartItemCRUDView

urlpatterns = [
    path("carts/<int:cart_id>/cartitems", CartItemCRUDView.as_view()),
]
