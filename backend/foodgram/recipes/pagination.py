from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class EmptyPagination(pagination.PageNumberPagination):
    page_size = None

    def get_paginated_response(self, data):
        return Response(data)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
