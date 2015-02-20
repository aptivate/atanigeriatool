from __future__ import unicode_literals, absolute_import

from django.test.testcases import TestCase

from lscharts.embed import DEFAULT_COLORS
from main.charts import (
    Chart,
    NutritionChart,
    TechnologyChart,
    ProductivityPreATAChart,
    ProductivityDuringATAChart,
    ProductivityMarketPricesChart,
    PercentSalesDonutChart,
    AverageHouseholdSalesChart,
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
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain=None)
        self.assertNotIn('filters', args)

    def test_main_title_text_still_in_title_when_no_state_or_valuechain(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain=None)
        self.assertIn(chart.static_args['title'], args['title'])

    def test_nationwide_in_title_when_no_state_or_valuechain(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain=None)
        self.assertIn('Nationwide', args['title'])


class ChartStateTestMixin(object):
    def test_get_args_for_state_has_state_filter(self):
        chart = self.create_chart()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertSequenceEqual(args['filters'], [('State', 'Kogi')])

    def test_main_title_text_still_in_title_when_using_state_filter(self):
        chart = self.create_chart()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertIn(chart.static_args['title'], args['title'])

    def test_get_args_for_state_has_state_name_in_title(self):
        chart = self.create_chart()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertIn('Kogi', args['title'])


class ChartValueChainTestMixin(object):
    def test_get_args_for_valuechain_has_crop_filter(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertSequenceEqual(args['filters'], [('Crop', 'Rice')])

    def test_main_title_text_still_in_title_when_using_valuechain_filter(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertIn(chart.static_args['title'], args['title'])

    def test_get_args_for_valuechain_has_crop_name_in_title(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertIn('Rice', args['title'])


class GetChartTestMixin(object):
    def test_get_chart_returns_object_with_title_attribute_set(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain=None)
        chart_object = chart.get_chart(state=None, valuechain=None)
        self.assertEqual(args['title'], chart_object.title)


class CreateChartTestMixin(object):
    def create_chart(self):
        return self.chart_class()


class ChartTestMixin(CreateChartTestMixin, ChartSeeAllTestMixin,
                     ChartStateTestMixin, ChartValueChainTestMixin,
                     GetChartTestMixin):
    pass


class ChartTests(ChartTestMixin, TestCase):
    chart_class = Chart


class NutritionChartTests(ChartSeeAllTestMixin, ChartStateTestMixin,
                          GetChartTestMixin, CreateChartTestMixin, TestCase):
    chart_class = NutritionChart

    def test_get_args_for_state_has_state_filter(self):
        chart = self.create_chart()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertSequenceEqual(args['filters'], [('State', 'Kogi')])

    def test_get_args_for_rice_has_correct_filters(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='rice')
        filters = args['filters']
        for filter_detail in filters:
            self.assertEqual(filter_detail[0], 'Commodity')
            self.assertTrue(filter_detail[1].startswith('Rice'))

    def test_get_args_for_cassava_has_correct_filters(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='cassava')
        filters = args['filters']
        for filter_detail in filters:
            self.assertEqual(filter_detail[0], 'Commodity')
            self.assertTrue(filter_detail[1].startswith('Gari') or
                            filter_detail[1].startswith('Cassava'))


class TechnologyChartTests(ChartTestMixin, TestCase):
    chart_class = TechnologyChart


class ProductivityPreATAChartTests(GetChartTestMixin, CreateChartTestMixin, TestCase):
    chart_class = ProductivityPreATAChart

    def assert_crop_used(self, args):
        self.assertSequenceEqual(['Crop'], args['variables'])
        self.assertEqual('Crop', args['x_label'])
        self.assertTrue(args['title'].startswith('Crop'))
        self.assertEqual('Year', args['filters'][0][0])

    def test_see_all_args_uses_crop_variable(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain=None)
        self.assert_crop_used(args)

    def test_state_args_uses_crop_variable(self):
        chart = self.create_chart()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assert_crop_used(args)

    def test_valuechain_args_use_year_variable(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='cassava')
        self.assertSequenceEqual(['Year'], args['variables'])
        self.assertEqual('Year', args['x_label'])
        self.assertTrue(args['title'].startswith('Cassava'))
        self.assertEqual('Crop', args['filters'][0][0])


class ProductivityDuringATAChartTests(ChartSeeAllTestMixin, ChartStateTestMixin,
                                      GetChartTestMixin, CreateChartTestMixin, TestCase):
    chart_class = ProductivityDuringATAChart

    def test_setting_rice_as_crop_does_not_add_filters(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertNotIn('filters', args)

    def test_setting_cassava_as_crop_sets_not_available_message(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='cassava')
        self.assertIn('not_available_message', args)


class ProductivityMarketPricesChartTests(CreateChartTestMixin,
                                         GetChartTestMixin, TestCase):
    chart_class = ProductivityMarketPricesChart

    def test_filter_not_set_when_no_state_or_valuechain(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain=None)
        self.assertNotIn('filters', args)

    def test_main_title_text_still_in_title_when_no_state_or_valuechain(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain=None)
        self.assertIn(chart.static_args['title'], args['title'])

    def test_nationwide_not_in_title_when_no_state_or_valuechain(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain=None)
        self.assertNotIn('nationwide', args['title'])

    def test_setting_benue_as_state_sets_not_available_message(self):
        chart = self.create_chart()
        args = chart.get_args(state='benue', valuechain=None)
        self.assertIn('not_available_message', args)

    def test_setting_kogi_as_state_does_not_add_filter(self):
        chart = self.create_chart()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertNotIn('filters', args)

    def test_main_title_text_still_in_title_when_using_state_filter(self):
        chart = self.create_chart()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertIn(chart.static_args['title'], args['title'])

    def test_get_args_for_state_has_state_name_in_title(self):
        chart = self.create_chart()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertIn('Kogi', args['title'])

    def test_get_args_for_valuechain_has_crop_filter_for_rice(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertSequenceEqual(
            args['filters'],
            [('Crop', 'Rice (milled)'), ('Crop', 'Rice (paddy)')])

    def test_get_args_for_valuechain_has_crop_filter_for_cassava(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='cassava')
        self.assertSequenceEqual(
            args['filters'],
            [('Crop', 'Cassava'), ('Crop', 'Garri')])

    def test_main_title_text_still_in_title_when_using_valuechain_filter(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertIn(chart.static_args['title'], args['title'])

    def test_get_args_for_valuechain_has_crop_name_in_title(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertIn('Rice', args['title'])


# TODO: write tests properly if we keep this chart
class PercentSalesDonutChartTests(CreateChartTestMixin,
                                  GetChartTestMixin, TestCase):
    chart_class = PercentSalesDonutChart

    def create_chart(self, year=2010):
        return self.chart_class(year)

    def test_see_all_has_correct_filters_for_2010(self):
        chart = self.create_chart(2010)
        args = chart.get_args(state=None, valuechain=None)
        self.assertSequenceEqual(args['filters'], [('Year', '2010')])

    def test_see_all_has_correct_filters_for_2012(self):
        chart = self.create_chart(2012)
        args = chart.get_args(state=None, valuechain=None)
        self.assertSequenceEqual(args['filters'], [('Year', '2012')])

    def test_nationwide_in_title_when_no_state_or_valuechain(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain=None)
        self.assertIn('Nationwide', args['title'])

    def test_get_args_for_state_has_state_filter(self):
        chart = self.create_chart()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertSequenceEqual(
            args['filters'],
            [('Year', '2010'), ('State', 'Kogi')])

    def test_main_title_text_still_in_title_when_using_state_filter(self):
        chart = self.create_chart()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertIn(chart.static_args['title'], args['title'])

    def test_get_args_for_state_has_state_name_in_title(self):
        chart = self.create_chart()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertIn('Kogi', args['title'])

    def test_get_args_for_valuechain_has_crop_filter(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertSequenceEqual(
            args['filters'],
            [('Year', '2010'), ('Crop', 'Rice')])

    def test_main_title_text_still_in_title_when_using_valuechain_filter(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertIn(chart.static_args['title'], args['title'])

    def test_get_args_for_valuechain_has_crop_name_in_title(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertIn('Rice', args['title'])


class AverageHouseholdSalesChartTests(ChartTestMixin, TestCase):
    chart_class = AverageHouseholdSalesChart

    def test_get_args_for_valuechain_has_crop_filter(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertSequenceEqual(args['filters'], [('Crop', 'Rice')])

    def test_valuechain_args_has_different_dataset(self):
        """ The valuechain uses a different dataset as for:
        * valuechain - we get the value sold only for that crop and then we
          average.  So we need one row for each household_id/crop pair
        * others - we want the sum of all values sold by that household and
          then we average.  So we need one row for each household_id

        So we have prepared two different datasets and need to switch between
        them as required.
        """
        chart = self.create_chart()
        normal_args = chart.get_args(state=None, valuechain=None)
        rice_args = chart.get_args(state=None, valuechain='rice')
        self.assertNotEqual(normal_args['dataset'], rice_args['dataset'])
        self.assertNotEqual(normal_args['dataset_id'], rice_args['dataset_id'])


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


class ChartInheritanceTests(CreateChartTestMixin, TestCase):
    """Here we are checking and documenting the expected methods to override
    in Chart so that future users can have confidence"""
    chart_class = DummyChart

    def test_static_args_are_copied_into_args(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain=None)
        self.assertEqual(args['rabbit'], 'carrot')

    def test_static_args_are_copied_into_args_and_are_not_references(self):
        chart = self.create_chart()
        args1 = chart.get_args(state=None, valuechain=None)
        args2 = chart.get_args(state=None, valuechain=None)
        args1['rabbit'] = 'grass'
        self.assertEqual(args2['rabbit'], 'carrot')

    def test_update_args_for_see_all_is_called_when_no_state_or_valuechain(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain=None)
        self.assertEqual(args['omnivore'], 'everything')

    def test_update_args_for_state_is_called_when_state_is_set(self):
        chart = self.create_chart()
        args = chart.get_args(state='kogi', valuechain=None)
        self.assertEqual(args['cow'], 'grass')

    def test_update_args_for_valuechain_is_called_when_valuechain_is_set(self):
        chart = self.create_chart()
        args = chart.get_args(state=None, valuechain='rice')
        self.assertEqual(args['wolf'], 'sheep')
