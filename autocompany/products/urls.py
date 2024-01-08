from django.urls import path

from .views import Products, Product

urlpatterns = [
    path("", Products.as_view(), name="get-all-products"),
    path("<int:pk>/", Product.as_view(), name="get-product-detail"),
]
