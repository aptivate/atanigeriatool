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

    def test_indicators_comma_returns_comma_separated_list(self):
        ecs = EmbedChartSettings(indicators=['afilter', 'bfilter'])
        self.assertEqual('afilter,bfilter', ecs.indicators_comma())

    def test_colors_comma_returns_comma_separated_list_with_hash_prefix(self):
        ecs = EmbedChartSettings(colors=['123456', '789ABC'])
        self.assertEqual('#123456,#789ABC', ecs.colors_comma())

    def test_get_query_params_does_not_have_secondary_operations_key_when_not_set(self):
        ecs = EmbedChartSettings()
        self.assertNotIn('secondaryOperation', ecs._get_query_params())

    def test_get_query_params_does_have_secondary_operations_key_when_is_set(self):
        ecs = EmbedChartSettings(secondary_operation='avg')
        self.assertIn('secondaryOperation', ecs._get_query_params())

    def test_explore_url_produces_correct_url(self):
        ecs = EmbedChartSettings()
        self.assertEqual(
            'http://ata.livestories.com/guest/chart?variables=Crop'
            '&colors=7a7654&colors=1d976b&colors=00a65d&colors=72bf44'
            '&colors=fff200&colors=faa61a&colors=f58220&colors=ef413d'
            '&colors=ed1c24&colors=a3238e&colors=5c2d91&colors=214009'
            '&dashboard=&title=Crop&indicators=__entry&chartType=pie'
            '&operation=count&dashId=&datasetId=54aff583a750b33915f0069c',
            ecs.explore_url())

    def test_explore_url_includes_filters(self):
        filters = [
            ('Term', 'ivory pieces'),
            ('Term', 'ivory scraps'),
            ('food', 'cassava')
        ]
        ecs = EmbedChartSettings(filters=filters)
        filter_url_part = ecs.filters_for_embed_link()
        self.assertIn(filter_url_part, ecs.explore_url())
