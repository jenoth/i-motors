from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from autocompany.cartitems.views import CartItemCRUDView

schema_view = get_schema_view(
    openapi.Info(
        title="I-MOTORS OpenAPI Specification (OAS)",
        default_version="v1",
        description="Open API(Swagger UI) definitions for I-MOTORS",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("customers/", include("autocompany.customers.urls")),
                path("products/", include("autocompany.products.urls")),
                path("carts/", include("autocompany.carts.urls")),
                path("orders/", include("autocompany.orders.urls")),
                path(
                    "customers/<int:customer_id>/carts/products/", CartItemCRUDView.as_view(), name="customer-cart-items"
                ),
            ]
        ),
    ),
    path("ui/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
