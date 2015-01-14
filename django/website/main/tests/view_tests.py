from __future__ import unicode_literals, absolute_import

from django.test.testcases import TestCase

from django_harness.fast_dispatch import FastDispatchMixin


class BasicViewTestsMixin(object):
    args = []

    def test_page_returns_status_code_200(self):
        response = self.fast_dispatch(self.url_name, url_args=self.args)
        self.assertEqual(200, response.status_code)

    def test_page_renders_without_error(self):
        response = self.fast_dispatch(self.url_name, url_args=self.args)
        response.render()
        # fail if there is an exception


class HomeViewTests(FastDispatchMixin, BasicViewTestsMixin, TestCase):
    url_name = 'home'


class StateFilterViewTests(FastDispatchMixin, BasicViewTestsMixin, TestCase):
    url_name = 'state_filter'
    args = ['kogi']


class ChartsViewTests(FastDispatchMixin, BasicViewTestsMixin, TestCase):
    url_name = 'charts'
