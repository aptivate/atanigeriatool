from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView

from lscharts.embed import EmbedChartSettings, DEFAULT_COLORS

COLOR_DURING_ATA = '1D976B'
COLOR_PRE_ATA = '7A7654'
COLOR_YIELD = '000'


def get_colors_with_overrides(*colors):
    new_colors = DEFAULT_COLORS[:]
    for i, color in enumerate(colors):
        new_colors[i] = color
    return new_colors

# TODO: move to settings?
DOMAIN = "ata.livestories.com"
CHARTS = {
    "nutrition": {
        "dataset": "29277fe2981511e4bbe006909bee25eb",
        "dataset_id": "54aff583a750b33915f0069c",
        'variables': ["Commodity", "year"],
        'indicators': ["Value"],
        'operation': "avg",
        'chart_type': "column",
        'y0_label': "Percentage of Households",
        'x_label': "Food, year",
        'title': "Percentage of households who consume food types in a typical week",
        "description":
            "DATASOURCE<br />"
            "Living Standard Measurement Study (LSMS)<br />"
            "World Bank<br />"
            "LSMS 2010 Household Post Planting Agriculture Survey (Section 7)<br />"
            "LSMS 2012 Household Post Planting Agriculture Survey (Section 7)<br />"
            "Processed tabular data powering this visualization",
    },
    "technology": {
        "dataset": "9e3d0cd49d7e11e4a93606909bee25eb",
        "dataset_id": "54b909c7a750b30f24f31db7",
        'variables': ["Technology", "year"],
        'indicators': ["Value"],
        'operation': "avg",
        'chart_type': "column",
        'y0_label': "Percentage of farmers",
        'x_label': "Technology, year",
        'title': "Percentage of farmers who use technologies",
        "description":
            "DATASOURCE<br />"
            "LSMS 2010<br />"
            "Post Planting Agriculture Survey (Section 11c)<br />"
            "LSMS 2012<br />"
            "Post Planting Agriculture Survey (Section 11c)<br />"
            "Processed tabular data powering this visualization",
    },
    "productivity_pre_ata": {
        "dataset": "8ba9c30ca16e11e4927006909bee25eb",
        "dataset_id": "54bfa4b9a750b3418651e0fc",
        'indicators': ["Production", "Yield Per Hectare"],
        'operation': "sum",
        'secondary_operation': "avg",
        'chart_type': "column",
        'y0_label': "Total production (metric tonnes)",
        'y1_label': "Average yield (metric tonnes/hectare)",
        'colors': get_colors_with_overrides(COLOR_PRE_ATA, COLOR_YIELD),
        "description":
            "DATASOURCE<br />"
            "Annual Abstract of Statistics, 2012<br />"
            "National Bureau of Statistics<br />"
            "Federal Republic of Nigeria",
    },
    "productivity_during_ata": {
        "dataset": "d4aa5ffaa09511e4a41406909bee25eb",
        "dataset_id": "54be3923a750b3418651e0d9",
        'variables': ["season"],
        'indicators': ["production", "yield"],
        'operation': "sum",
        'secondary_operation': "avg",
        'chart_type': "column",
        'y0_label': "Total production (metric tonnes)",
        'y1_label': "Average yield (metric tonnes/hectare)",
        'x_label': "Season and year",
        'title': "Rice production and yield during ATA",
        'colors': get_colors_with_overrides(COLOR_DURING_ATA, COLOR_YIELD),
        "description":
            "DATASOURCE<br />"
            "ATA Briefing to the Honorable Minister of Agriculture<br />"
            "Based on Cellulante data",
    },
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
        context['current_filter'] = self.get_current_filter(state, valuechain)
        return context

    def get_filter_title(self, state, valuechain):
        if state:
            return state
        elif valuechain:
            return "%s Value Chain" % valuechain
        else:
            return None

    def get_current_filter(self, state, valuechain):
        if state:
            return state
        elif valuechain:
            return valuechain
        else:
            return 'all'

    def get_generic_args(self, chart_type):
        chart_info = {'domain': DOMAIN}
        chart_info.update(CHARTS[chart_type])
        return chart_info

    def get_nutrition_args(self, state, valuechain):
        args = self.get_generic_args('nutrition')
        if state:
            args['filters'] = [('state', state)]
            args['title'] += " ({0} only)".format(state.capitalize())
        elif valuechain:
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
            args['title'] += " ({0} groups only, nationwide)".format(valuechain.capitalize())
        else:
            args['title'] += " (nationwide)"
        return args

    def get_technology_args(self, state, valuechain):
        args = self.get_generic_args('technology')
        if state:
            args['filters'] = [('state', state)]
            args['title'] += " ({0} only)".format(state.capitalize())
        elif valuechain:
            args['filters'] = [('crop', valuechain)]
            args['title'] += " ({0} farmers only, nationwide)".format(valuechain.capitalize())
        else:
            args['title'] += " (nationwide)"
        return args

    def get_productivity_pre_ata_args(self, state, valuechain):
        args = self.get_generic_args('productivity_pre_ata')
        if valuechain:  # chart for crop by year
            args.update({
                'variables': ["Year"],
                'x_label': "Year",
                'title': "{0} production and yield pre ATA (nationwide)".
                         format(valuechain.capitalize()),
                'filters': [('Crop', valuechain.capitalize())]
            })
        else:
            args.update({
                'variables': ["Crop"],
                'title': "Crop production and yield pre ATA",
                'x_label': "Crop",
            })
            if state:
                args['title'] += " (Data cannot be filtered by {0})".format(state.capitalize())
            else:
                args['title'] += " (nationwide)"
            args['filters'] = [('Year', 2009)]
        return args

    def get_productivity_during_ata_args(self, state, valuechain):
        args = self.get_generic_args('productivity_during_ata')
        if state:
            args['filters'] = [('state', state)]
            args['title'] += " ({0} only)".format(state.capitalize())
        elif valuechain:
            if valuechain == 'cassava':
                args['not_available_message'] = \
                    "These data are available for Rice only"
                args['title'] = "Cassava production and yield during ATA (nationwide)"
        else:
            args['title'] += " (nationwide)"
        return args

    def get_charts(self, state, valuechain):
        return {
            'nutrition':
                EmbedChartSettings(**self.get_nutrition_args(state, valuechain)),
            'technology':
                EmbedChartSettings(**self.get_technology_args(state, valuechain)),
            'productivity_pre_ata':
                EmbedChartSettings(**self.get_productivity_pre_ata_args(state, valuechain)),
            'productivity_during_ata':
                EmbedChartSettings(**self.get_productivity_during_ata_args(state, valuechain)),
        }
