import math

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response

from .models import Product as ProductModel
from .serializers import ProductSerializer

page_query_param_in_product_retrieval_endpoint = openapi.Parameter(
    name="page",
    in_=openapi.IN_QUERY,
    required=False,
    type=openapi.TYPE_NUMBER,
    description="Page number of the pagination. Minimum page number is  1.",
)
limit_query_param_in_product_retrieval_endpoint = openapi.Parameter(
    name="limit",
    in_=openapi.IN_QUERY,
    required=False,
    type=openapi.TYPE_NUMBER,
    description="Page limit of the pagination. Minimum page limit is  1.",
)
search_query_param_in_product_retrieval_endpoint = openapi.Parameter(
    name="search",
    in_=openapi.IN_QUERY,
    required=False,
    type=openapi.TYPE_STRING,
    description="Search text of the product.",
)
query_params_of_product_retrieval_endpoint = [
    page_query_param_in_product_retrieval_endpoint,
    limit_query_param_in_product_retrieval_endpoint,
    search_query_param_in_product_retrieval_endpoint,
]


class Product(generics.RetrieveAPIView):
    """Default RetrieveAPIView to get a product for a given product id"""

    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer


class Products(generics.GenericAPIView):
    """GenericAPIView for getting all the products by providing pagination and search query"""

    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(manual_parameters=query_params_of_product_retrieval_endpoint)
    def get(self, request):
        """GET controller for getting all the filtered and paginated products"""
        # if we do not provide page query parameter then we will get None. But, we provide 1 as default value.
        # If we provide page query parameter without a value then we will get empty string
        # page or limit query params must be a natural number(positive integer)
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        products_query_set = ProductModel.objects.all()
        no_of_products = products_query_set.count()
        if search_param:
            products_query_set = products_query_set.filter(name__icontains=search_param)
        serializer = self.serializer_class(products_query_set[start_num:end_num], many=True)
        return Response(
            {
                "total_products": no_of_products,
                "current_page": page_num,
                "last_page": math.ceil(no_of_products / limit_num),
                "products": serializer.data,
            }
        )
