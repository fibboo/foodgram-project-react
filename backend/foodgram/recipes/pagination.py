from rest_framework import pagination
from rest_framework.response import Response


class EmptyPagination(pagination.PageNumberPagination):
    page_size = None

    def get_paginated_response(self, data):
        return Response(data)
