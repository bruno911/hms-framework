from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNumberCountPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = self.get_page_size(request=request)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'page_size': self.page_size,
            'count': self.page.paginator.count,
            'pages': self.page.paginator.num_pages,
            'page_number': self.page.number,
            'page_count': len(data),
            'results': data
        })


class TinyPagination(PageNumberCountPagination):
    page_size = 25


class SmallPagination(PageNumberCountPagination):
    page_size = 100


class MediumPagination(PageNumberCountPagination):
    page_size = 500


class LargePagination(PageNumberCountPagination):
    page_size = 2500


class HugePagination(PageNumberCountPagination):
    page_size = 5000



