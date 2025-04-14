from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from utils.api.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from utils.middleware.schema_middleware import CustomAutoSchema

# ------------------------------------ Components ------------------------------------ #


class PageSizePagination(PageNumberPagination):
    page_size_query_param = "page_size"


class CustomPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "page_size"
    # page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]


# --------------------------------------- Views -------------------------------------- #


class CustomRetrieveAPIView(RetrieveAPIView):
    schema = CustomAutoSchema()


class CustomCreateAPIView(CreateAPIView):
    schema = CustomAutoSchema()


class CustomListAPIView(ListAPIView):
    pagination_class = CustomPagination
    schema = CustomAutoSchema(_api_type="List")
