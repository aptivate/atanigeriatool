from __future__ import unicode_literals, absolute_import

from django.test.testcases import TestCase

from django_harness.fast_dispatch import FastDispatchMixin

from main.views import HomeView


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

    def test_get_charts_does_not_set_filter(self):
        view = HomeView()
        charts = view.get_charts(state=None, valuechain=None)
        self.assertIsNone(charts['nutrition'].filters)

    def test_get_filter_title_returns_none_for_no_filter(self):
        view = HomeView()
        filter_title = view.get_filter_title(state=None, valuechain=None)
        self.assertIsNone(filter_title)

    def test_get_current_filter_returns_all_for_no_filter(self):
        view = HomeView()
        self.assertEqual(
            'all',
            view.get_current_filter(state=None, valuechain=None)
        )


class StateFilterViewTests(FastDispatchMixin, BasicViewTestsMixin, TestCase):
    url_name = 'state_filter'
    args = ['kogi']

    def test_get_charts_sets_filter(self):
        view = HomeView()
        charts = view.get_charts(state='kogi', valuechain=None)
        self.assertTrue(hasattr(charts['nutrition'], 'filters'))

    def test_get_filter_title_returns_state_name(self):
        view = HomeView()
        filter_title = view.get_filter_title(state='kogi', valuechain=None)
        self.assertEqual('kogi', filter_title)

    def test_get_current_filter_returns_state_name_for_state_filter(self):
        view = HomeView()
        self.assertEqual(
            'kogi',
            view.get_current_filter(state='kogi', valuechain=None)
        )


class ValuechainFilterViewTests(FastDispatchMixin, BasicViewTestsMixin, TestCase):
    url_name = 'valuechain_filter'
    args = ['rice']

    def test_get_charts_sets_filter(self):
        view = HomeView()
        charts = view.get_charts(state=None, valuechain='rice')
        self.assertTrue(hasattr(charts['nutrition'], 'filters'))

    def test_get_filter_title_returns_filter_chain_name(self):
        view = HomeView()
        filter_title = view.get_filter_title(state=None, valuechain='cassava')
        self.assertIn('cassava', filter_title.lower())

    def test_get_current_filter_returns_valuechain_name_for_valuechain_filter(self):
        view = HomeView()
        self.assertEqual(
            'rice',
            view.get_current_filter(state=None, valuechain='rice')
        )
