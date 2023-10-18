from rest_framework.pagination import PageNumberPagination


class ApprovedMembersPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "page_size"


class GroupListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
