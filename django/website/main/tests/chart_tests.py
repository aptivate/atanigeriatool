from __future__ import unicode_literals, absolute_import

from django.test.testcases import TestCase

from lscharts.embed import DEFAULT_COLORS
from main.charts import (
    Chart,
    NutritionChart,
    TechnologyChart,
    ProductivityPreATAChart,
    ProductivityDuringATAChart,
    get_colors_with_overrides
)


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


class ChartSeeAllTestMixin(object):
    def test_filter_not_set_when_no_state_or_valuechain(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain=None)
        self.assertNotIn('filters', args)

    def test_nationwide_in_title_when_no_state_or_valuechain(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain=None)
        self.assertIn('nationwide', args['title'])


class ChartStateTestMixin(object):
    def test_get_args_for_state_has_state_filter(self):
        chart = self.chart_class()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertSequenceEqual(args['filters'], [('state', 'kogi')])

    def test_get_args_for_state_has_state_name_in_title(self):
        chart = self.chart_class()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertIn('Kogi', args['title'])


class ChartValueChainTestMixin(object):
    def test_get_args_for_valuechain_has_crop_filter(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertSequenceEqual(args['filters'], [('crop', 'rice')])

    def test_get_args_for_valuechain_has_crop_name_in_title(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertIn('Rice', args['title'])


class ChartTestMixin(ChartSeeAllTestMixin, ChartStateTestMixin,
                     ChartValueChainTestMixin):
    pass


class ChartTests(ChartTestMixin, TestCase):
    chart_class = Chart


class NutritionChartTests(ChartSeeAllTestMixin, ChartStateTestMixin, TestCase):
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


class ProductivityPreATAChartTests(TestCase):
    chart_class = ProductivityPreATAChart

    def assert_crop_used(self, args):
        self.assertSequenceEqual(['Crop'], args['variables'])
        self.assertEqual('Crop', args['x_label'])
        self.assertTrue(args['title'].startswith('Crop'))
        self.assertEqual('Year', args['filters'][0][0])

    def test_see_all_args_uses_crop_variable(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain=None)
        self.assert_crop_used(args)

    def test_state_args_uses_crop_variable(self):
        chart = self.chart_class()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assert_crop_used(args)

    def test_valuechain_args_use_year_variable(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain='cassava')
        self.assertSequenceEqual(['Year'], args['variables'])
        self.assertEqual('Year', args['x_label'])
        self.assertTrue(args['title'].startswith('Cassava'))
        self.assertEqual('Crop', args['filters'][0][0])


class ProductivityDuringATAChartTests(ChartSeeAllTestMixin,
                                      ChartStateTestMixin, TestCase):
    chart_class = ProductivityDuringATAChart

    def test_setting_rice_as_crop_does_not_add_filters(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertNotIn('filters', args)

    def test_setting_cassava_as_crop_sets_not_available_message(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain='cassava')
        self.assertIn('not_available_message', args)


class DummyChart(Chart):
    static_args = {
        'rabbit': 'carrot'
    }

    def update_args_for_state(self, args, state):
        args['cow'] = 'grass'

    def update_args_for_valuechain(self, args, valuechain):
        args['wolf'] = 'sheep'

    def update_args_for_see_all(self, args):
        args['omnivore'] = 'everything'


class ChartInheritanceTests(TestCase):
    """Here we are checking and documenting the expected methods to override
    in Chart so that future users can have confidence"""
    chart_class = DummyChart

    def test_static_args_are_copied_into_args(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain=None)
        self.assertEqual(args['rabbit'], 'carrot')

    def test_static_args_are_copied_into_args_and_are_not_references(self):
        chart = self.chart_class()
        args1 = chart.get_args(state=None, valuechain=None)
        args2 = chart.get_args(state=None, valuechain=None)
        args1['rabbit'] = 'grass'
        self.assertEqual(args2['rabbit'], 'carrot')

    def test_update_args_for_see_all_is_called_when_no_state_or_valuechain(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain=None)
        self.assertEqual(args['omnivore'], 'everything')

    def test_update_args_for_state_is_called_when_state_is_set(self):
        chart = self.chart_class()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertEqual(args['cow'], 'grass')

    def test_update_args_for_valuechain_is_called_when_valuechain_is_set(self):
        chart = self.chart_class()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertEqual(args['wolf'], 'sheep')
