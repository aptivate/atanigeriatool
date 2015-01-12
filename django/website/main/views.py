from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView

from lscharts.embed import EmbedChartSettings


# NOT included in main/urls.py - included directly in the root urls.py
class HomeView(TemplateView):
    template_name = 'main/homepage.html'
    # TODO: move to settings
    dataset = "29277fe2981511e4bbe006909bee25eb"
    domain = "ata.livestories.com"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['food_consumed_chart'] = EmbedChartSettings(
            dataset=self.dataset,
            domain=self.domain,
            variables="Commodity,year",
            indicators="Value",
            operation="avg",
            chart_type="column",
            legend="true",
            data_labels="true",
            text="Percentage of households who consume each foodstuff, in 2010 and 2012",
        )
        return context


class ChartsView(TemplateView):
    template_name = 'main/charts.html'
    # move to settings
    dataset = "29277fe2981511e4bbe006909bee25eb"
    domain = "ata.livestories.com"

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)
        context['test_chart'] = EmbedChartSettings(
            dataset=self.dataset,
            domain=self.domain,
            variables="Commodity,year",
            indicators="Value",
            operation="avg",
            chart_type="column",
            legend="true",
            data_labels="true",
            text="Percentage of households who consume each foodstuff, in 2010 and 2012",
        )
        """context['test_chart'] = EmbedChartSettings(
            dataset=self.dataset,
            domain=self.domain,
            variables="state,Commodity",
            indicators="Value",
            operation="avg",
            chart_type="stackedcolumn",
            legend="true",
            text="Average value across state, food type",
            filters=['benue', 'kogi'],
            filter_type='state'
        )"""
        return context
