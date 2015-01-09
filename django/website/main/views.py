from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView

from lscharts.embed import EmbedChartSettings


# NOT included in main/urls.py - included directly in the root urls.py
class HomeView(TemplateView):
    template_name = 'main/homepage.html'


class ChartsView(TemplateView):
    template_name = 'main/charts.html'
    # move to settings
    dataset = "5d50a14c97fa11e482e606909bee25eb"
    domain = "ata.livestories.com"

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)
        context['test_chart'] = EmbedChartSettings(
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
        )
        context['test_chart2'] = EmbedChartSettings(
            dataset=self.dataset,
            domain=self.domain,
            variables="Commodity",
            indicators="Value",
            operation="sum",
            chart_type="pie",
            text="Relative amounts of crop consumed",
        )
        return context
