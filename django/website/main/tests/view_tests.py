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
        self.assertFalse(hasattr(charts['nutrition'], 'filters'))


class StateFilterViewTests(FastDispatchMixin, BasicViewTestsMixin, TestCase):
    url_name = 'state_filter'
    args = ['kogi']

    def test_get_charts_sets_filter(self):
        view = HomeView()
        charts = view.get_charts(state='kogi', valuechain=None)
        self.assertTrue(hasattr(charts['nutrition'], 'filters'))

    def test_get_nutrition_args_for_state_has_state_filter(self):
        view = HomeView()
        args = view.get_nutrition_args(state='kogi', valuechain=None)
        self.assertSequenceEqual(args['filters'], [('state', 'kogi')])


class ValuechainFilterViewTests(FastDispatchMixin, BasicViewTestsMixin, TestCase):
    url_name = 'valuechain_filter'
    args = ['rice']

    def test_get_charts_sets_filter(self):
        view = HomeView()
        charts = view.get_charts(state=None, valuechain='rice')
        self.assertTrue(hasattr(charts['nutrition'], 'filters'))

    def test_get_nutrition_args_for_rice_has_correct_filters(self):
        view = HomeView()
        args = view.get_nutrition_args(state=None, valuechain='rice')
        filters = args['filters']
        for filter_detail in filters:
            self.assertEqual(filter_detail[0], 'Commodity')
            self.assertTrue(filter_detail[1].startswith('Rice'))

    def test_get_nutrition_args_for_cassava_has_correct_filters(self):
        view = HomeView()
        args = view.get_nutrition_args(state=None, valuechain='cassava')
        filters = args['filters']
        for filter_detail in filters:
            self.assertEqual(filter_detail[0], 'Commodity')
            self.assertTrue(filter_detail[1].startswith('Gari') or
                            filter_detail[1].startswith('Cassava'))
