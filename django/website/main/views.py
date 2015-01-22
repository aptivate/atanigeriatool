from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView

from lscharts.embed import EmbedChartSettings, DEFAULT_COLORS

# TODO: move to settings?
DOMAIN = "ata.livestories.com"
DATASETS = {
    "nutrition": "29277fe2981511e4bbe006909bee25eb",
    "technology": "9e3d0cd49d7e11e4a93606909bee25eb",
    "productivity": "d4aa5ffaa09511e4a41406909bee25eb",
    "productivity2": "8ba9c30ca16e11e4927006909bee25eb",
}
DATASET_IDS = {
    "nutrition": "54aff583a750b33915f0069c",
    "technology": "54b909c7a750b30f24f31db7",
    "productivity": "54be3923a750b3418651e0d9",
    "productivity2": "54bfa4b9a750b3418651e0fc",
}


# NOT included in main/urls.py - included directly in the root urls.py
class HomeView(TemplateView):
    template_name = 'main/homepage.html'

    def get_context_data(self, **kwargs):
        state = kwargs.get('state', None)
        valuechain = kwargs.get('valuechain', None)
        context = super(HomeView, self).get_context_data(**kwargs)
        context['charts'] = self.get_charts(state, valuechain)
        context['filter_title'] = self.get_filter_title(state, valuechain)
        context['state'] = state
        context['valuechain'] = valuechain
        return context

    def get_filter_title(self, state, valuechain):
        if state:
            return state
        elif valuechain:
            return "%s Value Chain" % valuechain
        else:
            return None

    def get_generic_args(self, chart_type):
        return {
            'dataset': DATASETS[chart_type],
            'dataset_id': DATASET_IDS[chart_type],
            'domain': DOMAIN,
        }

    def get_nutrition_args(self, state, valuechain):
        args = self.get_generic_args('nutrition')
        args.update({
            'variables': ["Commodity", "year"],
            'indicators': ["Value"],
            'operation': "avg",
            'chart_type': "column",
            'title': "Percentage of households who consume each food type, in 2010 and 2012",
        })
        if state:
            args['filters'] = [('state', state)]
            args['title'] += " in " + state.capitalize()
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
            args['title'] += " ({0} value chain)".format(valuechain)
        return args

    def get_technology_args(self, state, valuechain):
        args = self.get_generic_args('technology')
        args.update({
            'variables': ["Technology", "year"],
            'indicators': ["Value"],
            'operation': "avg",
            'chart_type': "column",
            'title': "Percentage of households using technologies in 2010 and 2012",
        })
        if state:
            args['filters'] = [('state', state)]
            args['title'] += " in " + state.capitalize()
        if valuechain:
            args['filters'] = [('crop', valuechain)]
            args['title'] += " ({0} value chain)".format(valuechain)
        return args

    def get_productivity_args(self, state, valuechain):
        productivity_colors = DEFAULT_COLORS[:]
        productivity_colors[0] = '849E92'
        productivity_colors[1] = '949292'
        args = self.get_generic_args('productivity')
        args.update({
            'colors': productivity_colors,
            'variables': ["season"],
            'indicators': ["production", "yield"],
            'operation': "sum",
            'secondary_operation': "avg",
            'chart_type': "column",
            'title': "Total production and average of yield across season (rice only)",
        })
        if state:
            args['filters'] = [('state', state)]
            args['title'] += " in " + state.capitalize()
        # we ignore valuechain - we only have data for rice currently
        # so for rice we just show the full chart, while for cassava we
        # will show a message saying there is no data instead of a chart, but
        # the logic for that is in the template
        return args

    def get_productivity2_args(self, state, valuechain):
        productivity_colors = DEFAULT_COLORS[:]
        productivity_colors[0] = '849E92'
        productivity_colors[1] = '949292'
        args = self.get_generic_args('productivity2')
        args.update({
            'colors': productivity_colors,
            'variables': ["Crop"],
            'indicators': ["Production","Yield Per Hectare"],
            'operation': "sum",
            'secondary_operation': "avg",
            'chart_type': "column",
            'title': "Total production and average of yield across crop for all states",
        })
        args['filters'] = [('Year', 2009)]
        # if valuechain:
        # We get a quite different chart
        # We ignore state because this dataset was aggregated to national level.
        # so it will get hidden by logic in the template.
        return args

    def get_charts(self, state, valuechain):
        return {
            'nutrition':
                EmbedChartSettings(**self.get_nutrition_args(state, valuechain)),
            'technology':
                EmbedChartSettings(**self.get_technology_args(state, valuechain)),
            'productivity':
                EmbedChartSettings(**self.get_productivity_args(state, valuechain)),
            'productivity2':
                EmbedChartSettings(**self.get_productivity2_args(state, valuechain)),
        }
