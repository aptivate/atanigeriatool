from __future__ import unicode_literals, absolute_import

from django.test.testcases import TestCase

from lscharts.embed import EmbedChartSettings


class EmbedChartSettingsTests(TestCase):

    def test_filters_not_set_if_not_supplied_in_kwargs(self):
        ecs = EmbedChartSettings()
        self.assertFalse(hasattr(ecs, 'filters'))

    def test_filters_set_if_filters_and_filter_type_supplied_in_kwargs(self):
        ecs = EmbedChartSettings(filters=['afilter'], filter_type='type')
        self.assertTrue(hasattr(ecs, 'filters'))

    def test_format_filters_combines_filters_correctly(self):
        filters = [
            ('Term', 'ivory pieces'),
            ('Term', 'ivory scraps'),
            ('food', 'cassava')
        ]
        actual_output = EmbedChartSettings().format_filters(filters)
        expected_output = "filters.Term=ivory%20pieces&amp;filters.Term=ivory" \
            "%20scraps&amp;filters.food=cassava"
        self.assertEqual(expected_output, actual_output)
