from __future__ import unicode_literals, absolute_import

from django.test.testcases import TestCase

from lib.fast_dispatch import FastDispatchMixin


class BasicViewTestsMixin(object):

    def test_page_returns_status_code_200(self):
        response = self.fast_dispatch(self.url_name)
        self.assertEqual(200, response.status_code)

    def test_page_renders_without_error(self):
        response = self.fast_dispatch(self.url_name)
        response.render()
        # fail if there is an exception


class HomeViewTests(FastDispatchMixin, BasicViewTestsMixin, TestCase):
    url_name = 'home'


class ChartsViewTests(FastDispatchMixin, BasicViewTestsMixin, TestCase):
    url_name = 'charts'
