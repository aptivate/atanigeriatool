from __future__ import unicode_literals, absolute_import

from django.template.loader import render_to_string
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
        expected_output = "filters.Term=ivory%20pieces&filters.Term=ivory" \
            "%20scraps&filters.food=cassava"
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

    def test_get_explore_query_params_does_not_have_secondary_operations_key_when_not_set(self):
        ecs = EmbedChartSettings()
        self.assertNotIn('secondaryOperation', ecs._get_explore_query_params())

    def test_get_explore_query_params_does_have_secondary_operations_key_when_is_set(self):
        ecs = EmbedChartSettings(secondary_operation='avg')
        self.assertIn('secondaryOperation', ecs._get_explore_query_params())

    def test_get_explore_query_params_does_not_have_category_order_key_when_not_set(self):
        ecs = EmbedChartSettings(category_order=None)
        self.assertNotIn('categoryOrder', ecs._get_explore_query_params())

    def test_get_explore_query_params_does_have_category_order_key_when_is_set(self):
        ecs = EmbedChartSettings(category_order='alphabetical')
        self.assertIn('categoryOrder', ecs._get_explore_query_params())

    def test_not_available_message_not_set_unless_provided_in_params(self):
        self.assertEqual(None, EmbedChartSettings().not_available_message)

    def test_not_available_message_set_when_provided_in_params(self):
        self.assertEqual(
            "not available",
            EmbedChartSettings(
                not_available_message="not available"
            ).not_available_message
        )

    def test_explore_url_produces_correct_url(self):
        ecs = EmbedChartSettings()
        self.assertEqual(
            'http://ata.livestories.com/guest/chart?variables=Crop'
            '&amp;colors=7a7654&amp;colors=1d976b&amp;colors=00a65d&amp;colors=72bf44'
            '&amp;colors=fff200&amp;colors=faa61a&amp;colors=f58220&amp;colors=ef413d'
            '&amp;colors=ed1c24&amp;colors=a3238e&amp;colors=5c2d91&amp;colors=214009'
            '&amp;dashboard=&amp;title=Crop&amp;indicators=__entry&amp;chartType=pie'
            '&amp;operation=count&amp;dashId=&amp;datasetId=54aff583a750b33915f0069c'
            '&amp;categoryOrder=alphabetical',
            ecs.explore_url())

    def test_explore_url_includes_filters(self):
        filters = [
            ('Term', 'ivory pieces'),
            ('Term', 'ivory scraps'),
            ('food', 'cassava')
        ]
        ecs = EmbedChartSettings(filters=filters)
        filter_url_part = ecs.filters_for_embed_link().replace('&', '&amp;')
        self.assertIn(filter_url_part, ecs.explore_url())

    def test_bool_str_to_num_returns_1_for_true(self):
        ecs = EmbedChartSettings(data_labels="true")
        self.assertEqual(1, ecs._bool_str_to_num("data_labels"))
        ecs = EmbedChartSettings(data_labels="True")
        self.assertEqual(1, ecs._bool_str_to_num("data_labels"))

    def test_bool_str_to_num_returns_0_for_false(self):
        ecs = EmbedChartSettings(data_labels="false")
        self.assertEqual(0, ecs._bool_str_to_num("data_labels"))
        ecs = EmbedChartSettings(data_labels="False")
        self.assertEqual(0, ecs._bool_str_to_num("data_labels"))


class EmbeddedChartTemplateTests(TestCase):

    def test_not_available_message_replaces_chart_in_template(self):
        chart_section = render_to_string(
            'lscharts/embedded_chart.html',
            {'chart': EmbedChartSettings(not_available_message="not available")}
        )
        self.assertIn("not available", chart_section)
        self.assertNotIn("data-dataset", chart_section)
