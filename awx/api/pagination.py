# Copyright (c) 2015 Ansible, Inc.
# All Rights Reserved.

# Django REST Framework
from django.conf import settings
from rest_framework import pagination
from rest_framework.utils.urls import replace_query_param


class Pagination(pagination.PageNumberPagination):

    page_size_query_param = 'page_size'
    max_page_size = settings.MAX_PAGE_SIZE

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request and self.request.get_full_path() or ''
        url = url.encode('utf-8')
        page_number = self.page.next_page_number()
        return replace_query_param(self.cap_page_size(url), self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request and self.request.get_full_path() or ''
        url = url.encode('utf-8')
        page_number = self.page.previous_page_number()
        return replace_query_param(self.cap_page_size(url), self.page_query_param, page_number)

    def cap_page_size(self, url):
        if int(self.request.query_params.get(self.page_size_query_param, 0)) > self.max_page_size:
            url = replace_query_param(url, self.page_size_query_param, self.max_page_size)
        return url

    def get_html_context(self):
        context = super().get_html_context()
        context['page_links'] = [pl._replace(url=self.cap_page_size(pl.url))
                                 for pl in context['page_links']]

        return context
