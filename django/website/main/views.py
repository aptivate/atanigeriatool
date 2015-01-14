from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView

from lscharts.embed import EmbedChartSettings

# TODO: move to settings?
DOMAIN = "ata.livestories.com"
DATASETS = {
    "nutrition": "29277fe2981511e4bbe006909bee25eb",
}


# NOT included in main/urls.py - included directly in the root urls.py
class HomeView(TemplateView):
    template_name = 'main/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['charts'] = self.get_charts()
        return context

    def get_charts(self):
        return {
            'nutrition': EmbedChartSettings(
                dataset=DATASETS['nutrition'],
                domain=DOMAIN,
                variables="Commodity,year",
                indicators="Value",
                operation="avg",
                chart_type="column",
                legend="true",
                data_labels="true",
                text="Percentage of households who consume each food type, in 2010 and 2012",
            )
        }


class StateFilterView(TemplateView):
    template_name = 'main/homepage.html'
