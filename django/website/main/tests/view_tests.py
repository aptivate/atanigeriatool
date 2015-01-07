from __future__ import unicode_literals, absolute_import

from django.test.testcases import TestCase

from lib.fast_dispatch import FastDispatchMixin


class HomeViewTests(FastDispatchMixin, TestCase):

    def test_home_page_returns_status_code_200(self):
        response = self.fast_dispatch('home')
        self.assertEqual(200, response.status_code)

    def test_home_page_renders_without_error(self):
        response = self.fast_dispatch('home')
        response.render()
        # fail if there is an exception
