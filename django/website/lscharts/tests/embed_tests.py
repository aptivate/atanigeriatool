from __future__ import unicode_literals, absolute_import

from django.test.testcases import TestCase

from lscharts.embed import EmbedChartSettings


class EmbedChartSettingsTests(TestCase):

    def test_filter_for_embed_link_not_set_if_not_supplied_in_kwargs(self):
        self.assertEqual('', EmbedChartSettings().filters_for_embed_link())

    def test_filters_set_if_filters_and_filter_type_supplied_in_kwargs(self):
        filters = [
            ('Term', 'ivory pieces'),
        ]
        ecs = EmbedChartSettings(filters=filters)
        self.assertTrue(hasattr(ecs, 'filters'))

    def test_filter_for_embed_link_combines_filters_correctly(self):
        filters = [
            ('Term', 'ivory pieces'),
            ('Term', 'ivory scraps'),
            ('food', 'cassava')
        ]
        actual_output = EmbedChartSettings(filters=filters).filters_for_embed_link()
        expected_output = "filters.Term=ivory%20pieces&amp;filters.Term=ivory" \
            "%20scraps&amp;filters.food=cassava"
        self.assertEqual(expected_output, actual_output)

    def test_variables_comma_returns_comma_separated_list(self):
        ecs = EmbedChartSettings(variables=['afilter', 'bfilter'])
        self.assertEqual('afilter,bfilter', ecs.variables_comma())

    def test_variables_url_args_returns_filters_formatted_for_url(self):
        ecs = EmbedChartSettings(variables=['afilter', 'bfilter'])
        self.assertEqual('variables=afilter&variables=bfilter', ecs.variables_url_args())

    def test_indicators_comma_returns_comma_separated_list(self):
        ecs = EmbedChartSettings(indicators=['afilter', 'bfilter'])
        self.assertEqual('afilter,bfilter', ecs.indicators_comma())

    def test_indicators_url_args_returns_filters_formatted_for_url(self):
        ecs = EmbedChartSettings(indicators=['afilter', 'bfilter'])
        self.assertEqual('indicators=afilter&indicators=bfilter', ecs.indicators_url_args())

    def test_colors_comma_returns_comma_separated_list_with_hash_prefix(self):
        ecs = EmbedChartSettings(colors=['123456', '789ABC'])
        self.assertEqual('#123456,#789ABC', ecs.colors_comma())

    def test_colors_url_args_returns_filters_formatted_for_url(self):
        ecs = EmbedChartSettings(colors=['123456', '789ABC'])
        self.assertEqual('colors=123456&colors=789ABC', ecs.colors_url_args())
