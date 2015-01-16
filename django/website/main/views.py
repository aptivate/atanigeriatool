from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView

from lscharts.embed import EmbedChartSettings

# TODO: move to settings?
DOMAIN = "ata.livestories.com"
DATASETS = {
    "nutrition": "29277fe2981511e4bbe006909bee25eb",
    "technology": "60c7d2229d6e11e4a14406909bee25eb",
}


# NOT included in main/urls.py - included directly in the root urls.py
class HomeView(TemplateView):
    template_name = 'main/homepage.html'

    def get_context_data(self, **kwargs):
        state = kwargs.get('state', None)
        valuechain = kwargs.get('valuechain', None)
        context = super(HomeView, self).get_context_data(**kwargs)
        context['charts'] = self.get_charts(state, valuechain)
        return context

    def get_nutrition_args(self, state, valuechain):
        nutrition_args = {
            'dataset': DATASETS['nutrition'],
            'domain': DOMAIN,
            'variables': "Commodity,year",
            'indicators': "Value",
            'operation': "avg",
            'chart_type': "column",
            'legend': "true",
            'data_labels': "true",
            'text': "Percentage of households who consume each food type, in 2010 and 2012",
        }
        if state:
            nutrition_args['filters'] = [('state', state)]
            nutrition_args['text'] += " in %s" % state.capitalize()
        if valuechain:
            if valuechain == 'rice':
                nutrition_args['filters'] = [
                    ('Commodity', 'Rice - imported'),
                    ('Commodity', 'Rice - local')
                ]
            elif valuechain == 'cassava':
                nutrition_args['filters'] = [
                    ('Commodity', 'Cassava - roots'),
                    ('Commodity', 'Cassava flour'),
                    ('Commodity', 'Gari - white'),
                    ('Commodity', 'Gari - yellow')
                ]
            nutrition_args['text'] += " (%s value chain)" % valuechain
        return nutrition_args

    def get_technology_args(self, state, valuechain):
        args = {
            'dataset': DATASETS['technology'],
            'domain': DOMAIN,
            'variables': "Technology,year",
            'indicators': "Value",
            'operation': "avg",
            'chart_type': "column",
            'legend': "true",
            'data_labels': "true",
            'text': "Percentage of households using technologies in 2010 and 2012",
        }
        return args


    def get_charts(self, state, valuechain):
        return {
            'nutrition':
                EmbedChartSettings(**self.get_nutrition_args(state, valuechain)),
            'technology':
                EmbedChartSettings(**self.get_technology_args(state, valuechain)),
        }
