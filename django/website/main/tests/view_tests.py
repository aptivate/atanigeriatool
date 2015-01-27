from __future__ import unicode_literals, absolute_import

from django.test.testcases import TestCase

from django_harness.fast_dispatch import FastDispatchMixin

from lscharts.embed import DEFAULT_COLORS
from main.views import HomeView, get_colors_with_overrides


class GetColorsWithOverridesTests(TestCase):
    def test_get_colors_with_overrides_returns_default_colors_if_no_args(self):
        colors = get_colors_with_overrides()
        self.assertSequenceEqual(DEFAULT_COLORS, colors)

    def test_get_colors_with_overrides_changes_first_color_to_only_arg(self):
        colors = get_colors_with_overrides("123456")
        self.assertEqual("123456", colors[0])
        self.assertEqual(DEFAULT_COLORS[1], colors[1])
        self.assertEqual(DEFAULT_COLORS[2], colors[2])

    def test_get_colors_with_overrides_changes_two_colors_if_two_args(self):
        colors = get_colors_with_overrides("123456", "654321")
        self.assertEqual("123456", colors[0])
        self.assertEqual("654321", colors[1])
        self.assertEqual(DEFAULT_COLORS[2], colors[2])


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

    def test_get_nutrition_args_for_state_has_state_filter(self):
        view = HomeView()
        args = view.get_nutrition_args(state='kogi', valuechain=None)
        self.assertSequenceEqual(args['filters'], [('state', 'kogi')])

    def test_get_technology_args_for_state_has_state_filter(self):
        view = HomeView()
        args = view.get_technology_args(state='kogi', valuechain=None)
        self.assertSequenceEqual(args['filters'], [('state', 'kogi')])

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

    def test_get_technology_args_for_valuechain_has_crop_filter(self):
        view = HomeView()
        args = view.get_technology_args(state=None, valuechain='rice')
        self.assertSequenceEqual(args['filters'], [('crop', 'rice')])

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
