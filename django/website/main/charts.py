from __future__ import unicode_literals, absolute_import

from lscharts.embed import EmbedChartSettings, DEFAULT_COLORS


def get_colors_with_overrides(*colors):
    new_colors = DEFAULT_COLORS[:]
    for i, color in enumerate(colors):
        new_colors[i] = color
    return new_colors

COLOR_DURING_ATA = '1D976B'
COLOR_PRE_ATA = '7A7654'
COLOR_YIELD = '000'

TIME_SERIES_COLORS = get_colors_with_overrides(COLOR_PRE_ATA, COLOR_DURING_ATA)
PRE_ATA_COLORS = get_colors_with_overrides(COLOR_PRE_ATA, COLOR_YIELD)
DURING_ATA_COLORS = get_colors_with_overrides(COLOR_DURING_ATA, COLOR_YIELD)

# TODO: move to settings?
DOMAIN = "ata.livestories.com"


class Chart(object):
    static_args = {}

    def get_chart(self, state, valuechain):
        return EmbedChartSettings(**self.get_args(state, valuechain))

    def get_args(self, state, valuechain):
        args = {'domain': DOMAIN}
        # note that the update method *copies* the elements across
        args.update(self.static_args)
        if state:
            args = self.update_args_for_state(args, state)
        elif valuechain:
            args = self.update_args_for_valuechain(args, valuechain)
        else:
            args = self.update_args_for_see_all(args)
        return args

    def update_args_for_state(self, args, state):
        args['filters'] = [('state', state)]
        args['title'] += " ({0} only)".format(state.capitalize())

    def update_args_for_valuechain(self, args, valuechain):
        args['filters'] = [('crop', valuechain)]
        args['title'] += " ({0} farmers only, nationwide)".format(valuechain.capitalize())

    def update_args_for_see_all(self, args):
        args['title'] += " (nationwide)"


class NutritionChart(Chart):
    static_args = {
        "dataset": "29277fe2981511e4bbe006909bee25eb",
        "dataset_id": "54aff583a750b33915f0069c",
        'variables': ["Commodity", "year"],
        'indicators': ["Value"],
        'operation': "avg",
        'chart_type': "column",
        'y0_label': "Percentage of Households",
        'x_label': "Food, year",
        'colors': TIME_SERIES_COLORS,
        'title': "Percentage of households who consume food types in a typical week",
        "description":
            "DATASOURCE<br />"
            "Living Standard Measurement Study (LSMS)<br />"
            "World Bank<br />"
            "LSMS 2010 Household Post Planting Agriculture Survey (Section 7)<br />"
            "LSMS 2012 Household Post Planting Agriculture Survey (Section 7)<br />"
            "Processed tabular data powering this visualization",
    }
    valuechain_filters = {
        'rice': [
            ('Commodity', 'Rice - imported'),
            ('Commodity', 'Rice - local')
        ],
        'cassava': [
            ('Commodity', 'Cassava - roots'),
            ('Commodity', 'Cassava flour'),
            ('Commodity', 'Gari - white'),
            ('Commodity', 'Gari - yellow')
        ]
    }

    def update_args_for_valuechain(self, args, valuechain):
        args['filter'] = self.valuechain_filters[valuechain][:]
        args['title'] += " ({0} groups only, nationwide)".format(valuechain.capitalize())


class TechnologyChart(Chart):
    static_args = {
        "dataset": "9e3d0cd49d7e11e4a93606909bee25eb",
        "dataset_id": "54b909c7a750b30f24f31db7",
        'variables': ["Technology", "year"],
        'indicators': ["Value"],
        'operation': "avg",
        'chart_type': "column",
        'y0_label': "Percentage of farmers",
        'x_label': "Technology, year",
        'colors': TIME_SERIES_COLORS,
        'title': "Percentage of farmers who use technologies",
        "description":
            "DATASOURCE<br />"
            "LSMS 2010<br />"
            "Post Planting Agriculture Survey (Section 11c)<br />"
            "LSMS 2012<br />"
            "Post Planting Agriculture Survey (Section 11c)<br />"
            "Processed tabular data powering this visualization",
    }


class ProductivityPreATAChart(Chart):
    static_args = {
        "dataset": "8ba9c30ca16e11e4927006909bee25eb",
        "dataset_id": "54bfa4b9a750b3418651e0fc",
        'indicators': ["Production", "Yield Per Hectare"],
        'operation': "sum",
        'secondary_operation': "avg",
        'chart_type': "column",
        'y0_label': "Total production (metric tonnes)",
        'y1_label': "Average yield (metric tonnes/hectare)",
        'colors': PRE_ATA_COLORS,
        "description":
            "DATASOURCE<br />"
            "Annual Abstract of Statistics, 2012<br />"
            "National Bureau of Statistics<br />"
            "Federal Republic of Nigeria",
    }

    def update_args_for_state(self, args, state):
        self.update_args_for_general_chart(args)
        args['title'] += " (Data cannot be filtered by {0})".format(state.capitalize())

    def update_args_for_valuechain(self, args, valuechain):
        args.update({
            'variables': ["Year"],
            'x_label': "Year",
            'title': "{0} production and yield pre ATA (nationwide)".
                     format(valuechain.capitalize()),
            'filters': [('Crop', valuechain.capitalize())]
        })

    def update_args_for_see_all(self, args):
        self.update_args_for_general_chart(args)
        args['title'] += " (nationwide)"

    def update_args_for_general_chart(self, args):
        args.update({
            'variables': ["Crop"],
            'title': "Crop production and yield pre ATA",
            'x_label': "Crop",
            'filters': [('Year', 2009)],
        })


class ProductivityDuringATAChart(Chart):
    static_args = {
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
        'colors': DURING_ATA_COLORS,
        "description":
            "DATASOURCE<br />"
            "ATA Briefing to the Honorable Minister of Agriculture<br />"
            "Based on Cellulante data",
    }

    def update_args_for_valuechain(self, args, valuechain):
        if valuechain != 'rice':
            args['not_available_message'] = \
                "These data are available for Rice only"
            args['title'] = "{0} production and yield during ATA (nationwide)".format(
                            valuechain.capitalize())


def get_all_charts(state, valuechain):
    return {
        'nutrition': NutritionChart().get_chart(state, valuechain),
        'technology': TechnologyChart().get_chart(state, valuechain),
        'productivity_pre_ata': ProductivityPreATAChart().get_chart(state, valuechain),
        'productivity_during_ata': ProductivityDuringATAChart().get_chart(state, valuechain),
    }
