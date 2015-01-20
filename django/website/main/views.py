from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView

from lscharts.embed import EmbedChartSettings

# TODO: move to settings?
DOMAIN = "ata.livestories.com"
DATASETS = {
    "nutrition": "29277fe2981511e4bbe006909bee25eb",
    "technology": "9e3d0cd49d7e11e4a93606909bee25eb",
    "productivity": "d4aa5ffaa09511e4a41406909bee25eb",
}
DATASET_IDS = {
    "nutrition": "54aff583a750b33915f0069c",
    "technology": "54b909c7a750b30f24f31db7",
    "productivity": "54be3923a750b3418651e0d9",
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

    def get_generic_args(self, chart_type):
        return {
            'dataset': DATASETS[chart_type],
            'dataset_id': DATASET_IDS[chart_type],
            'domain': DOMAIN,
            'legend': "true",
            'data_labels': "true",
        }

    def get_nutrition_args(self, state, valuechain):
        args = self.get_generic_args('nutrition')
        args.update({
            'variables': ["Commodity", "year"],
            'indicators': ["Value"],
            'operation': "avg",
            'chart_type': "column",
            'text': "Percentage of households who consume each food type, in 2010 and 2012",
        })
        if state:
            args['filters'] = [('state', state)]
            args['text'] += " in " + state.capitalize()
        if valuechain:
            if valuechain == 'rice':
                args['filters'] = [
                    ('Commodity', 'Rice - imported'),
                    ('Commodity', 'Rice - local')
                ]
            elif valuechain == 'cassava':
                args['filters'] = [
                    ('Commodity', 'Cassava - roots'),
                    ('Commodity', 'Cassava flour'),
                    ('Commodity', 'Gari - white'),
                    ('Commodity', 'Gari - yellow')
                ]
            args['text'] += " ({0} value chain)".format(valuechain)
        return args

    def get_technology_args(self, state, valuechain):
        args = self.get_generic_args('technology')
        args.update({
            'variables': ["Technology", "year"],
            'indicators': ["Value"],
            'operation': "avg",
            'chart_type': "column",
            'text': "Percentage of households using technologies in 2010 and 2012",
        })
        if state:
            args['filters'] = [('state', state)]
            args['text'] += " in " + state.capitalize()
        if valuechain:
            args['filters'] = [('crop', valuechain)]
            args['text'] += " ({0} value chain)".format(valuechain)
        return args

    def get_productivity_args(self, state, valuechain):
        args = self.get_generic_args('productivity')
        args.update({
            'variables': ["season"],
            'indicators': ["production", "yield"],
            'operation': "sum",
            'secondary_operation': "avg",
            'chart_type': "column",
            'text': "Total production and average of yield across season",
        })
        if state:
            args['filters'] = [('state', state)]
            args['text'] += " in " + state.capitalize()
        if valuechain:
            args['filters'] = [('crop', valuechain)]
            args['text'] += " ({0} value chain)".format(valuechain)
        return args

    def get_charts(self, state, valuechain):
        return {
            'nutrition':
                EmbedChartSettings(**self.get_nutrition_args(state, valuechain)),
            'technology':
                EmbedChartSettings(**self.get_technology_args(state, valuechain)),
            'productivity':
                EmbedChartSettings(**self.get_productivity_args(state, valuechain)),
        }
