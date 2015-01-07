from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView

from lscharts.embed import EmbedChartSettings


# NOT included in main/urls.py - included directly in the root urls.py
class HomeView(TemplateView):
    template_name = 'main/homepage.html'


class ChartsView(TemplateView):
    template_name = 'main/charts.html'

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)
        context['test_chart'] = EmbedChartSettings(
            dataset="5b19fd0a92bf11e4acc406909bee25eb",
            variables="Crop",
            indicators="__entry",
            operation="count",
            chart_type="pie",
            domain="insight.livestories.com",
            text="Crop"
        )
        context['test_chart2'] = EmbedChartSettings(
            dataset="a00a9f40966c11e4871706909bee25eb",
            variables="Exporter",
            indicators="Exporter reported quantity",
            operation="sum",
            chart_type="column",
            domain="ata.livestories.com",
            text="Total Exporter reported quantity across Exporter"
        )
        return context
