from __future__ import unicode_literals, absolute_import

from django.test.testcases import TestCase

from lscharts.embed import DEFAULT_COLORS
from main.charts import (
    Chart, NutritionChart, TechnologyChart,
    get_colors_with_overrides)


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


class ChartTestMixin(object):
    chart_class = Chart

    def test_filter_not_set_when_no_state_or_valuechain(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain=None)
        self.assertNotIn('filters', args)


class ChartTests(ChartTestMixin, TestCase):
    pass


class NutritionChartTests(ChartTestMixin, TestCase):
    chart_class = NutritionChart

    def test_get_args_for_state_has_state_filter(self):
        chart = self.chart_class()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertSequenceEqual(args['filters'], [('state', 'kogi')])

    def test_get_args_for_rice_has_correct_filters(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain='rice')
        filters = args['filters']
        for filter_detail in filters:
            self.assertEqual(filter_detail[0], 'Commodity')
            self.assertTrue(filter_detail[1].startswith('Rice'))

    def test_get_args_for_cassava_has_correct_filters(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain='cassava')
        filters = args['filters']
        for filter_detail in filters:
            self.assertEqual(filter_detail[0], 'Commodity')
            self.assertTrue(filter_detail[1].startswith('Gari') or
                            filter_detail[1].startswith('Cassava'))


class TechnologyChartTests(ChartTestMixin, TestCase):
    chart_class = TechnologyChart

    def test_get_technology_args_for_state_has_state_filter(self):
        chart = self.chart_class()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertSequenceEqual(args['filters'], [('state', 'kogi')])

    def test_get_args_for_valuechain_has_crop_filter(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertSequenceEqual(args['filters'], [('crop', 'rice')])
