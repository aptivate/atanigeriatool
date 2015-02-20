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
COLOR_BACKGROUND = "DDDDDD"
COLOR_MARKET_PRICE1 = "57CF93"
COLOR_MARKET_PRICE2 = "158232"
COLOR_MARKET_PRICE3 = "55615C"
COLOR_MARKET_PRICE4 = "A2AD9C"

TIME_SERIES_COLORS = get_colors_with_overrides(COLOR_PRE_ATA, COLOR_DURING_ATA)
PRE_ATA_COLORS = get_colors_with_overrides(COLOR_PRE_ATA, COLOR_YIELD)
DURING_ATA_COLORS = get_colors_with_overrides(COLOR_DURING_ATA, COLOR_YIELD)
PRE_ATA_ONLY_COLORS = get_colors_with_overrides(COLOR_PRE_ATA, COLOR_BACKGROUND)
DURING_ATA_ONLY_COLORS = get_colors_with_overrides(COLOR_DURING_ATA, COLOR_BACKGROUND)
MARKET_PRICE_COLORS = get_colors_with_overrides(
    COLOR_MARKET_PRICE1, COLOR_MARKET_PRICE2, COLOR_MARKET_PRICE3, COLOR_MARKET_PRICE4)

# TODO: move to settings?
DOMAIN = "ata.livestories.com"


class Chart(object):
    static_args = {
        'title': 'Dummy Title',
    }

    def get_chart(self, state, valuechain):
        return EmbedChartSettings(**self.get_args(state, valuechain))

    def get_args(self, state, valuechain):
        args = {'domain': DOMAIN}
        # note that the update method *copies* the elements across
        args.update(self.static_args)
        if state:
            self.update_args_for_state(args, state)
        elif valuechain:
            self.update_args_for_valuechain(args, valuechain)
        else:
            self.update_args_for_see_all(args)
        return args

    def update_args_for_state(self, args, state):
        args['filters'] = [('State', state.capitalize())]
        args['title'] += " ({0} Only)".format(state.capitalize())

    def update_args_for_valuechain(self, args, valuechain):
        args['filters'] = [('Crop', valuechain.capitalize())]
        args['title'] += " ({0} Farmers Only, Nationwide)".format(valuechain.capitalize())

    def update_args_for_see_all(self, args):
        args['title'] += " (Nationwide)"


class NutritionChart(Chart):
    static_args = {
        "dataset": "29277fe2981511e4bbe006909bee25eb",
        "dataset_id": "54aff583a750b33915f0069c",
        'variables': ["Commodity", "Year"],
        'indicators': ["Value"],
        'operation': "avg",
        'chart_type': "column",
        'y0_label': "Percentage of Households",
        'x_label': "Food and Year",
        'colors': TIME_SERIES_COLORS,
        'title': "Percentage of Households that Consume Food Types in a Typical Week",
        'confidence': 'High',
        "description":
            "Datasource:<br />"
            "LSMS Post Planting Household Survey Section "
            "7b, year 2012 and 2010<br />"
            "Primary Data<br />"
            "5000 Households<br />",
    }
    valuechain_filters = {
        'rice': [
            ('Commodity', 'Rice - Imported'),
            ('Commodity', 'Rice - Local')
        ],
        'cassava': [
            ('Commodity', 'Cassava - Roots'),
            ('Commodity', 'Cassava - Flour'),
            ('Commodity', 'Gari - White'),
            ('Commodity', 'Gari - Yellow')
        ]
    }

    def update_args_for_valuechain(self, args, valuechain):
        args['filters'] = self.valuechain_filters[valuechain][:]
        args['title'] += " ({0} Groups Only, Nationwide)".format(valuechain.capitalize())


class TechnologyChart(Chart):
    static_args = {
        "dataset": "9e3d0cd49d7e11e4a93606909bee25eb",
        "dataset_id": "54b909c7a750b30f24f31db7",
        'variables': ["Technology", "Year"],
        'indicators': ["Value"],
        'operation': "avg",
        'chart_type': "column",
        'y0_label': "Percentage of Farmers",
        'x_label': "Technology and Year",
        'colors': TIME_SERIES_COLORS,
        'title': "Percentage of Farmers Who Use Technologies",
        'confidence': 'High',
        "description":
            "Datasource:<br />"
            "LSMS Post Planting Agriculture Survey Section "
            "11c, year 2012 and 2010<br />"
            "Primary Data<br />"
            "5000 Households<br />",
    }


class SeedAcquisitionChart(Chart):
    static_args = {
        "dataset": "34711b02b84e11e49da206909bee25eb",
        "dataset_id": "54e604f2a750b363fa334e6e",
        'variables': ["Year"],
        'indicators': ["Seed Reuse", "Seed Purchased", "Free Seed"],
        'operation': "avg",
        'secondary_operation': "avg",
        'chart_type': "column",
        'y0_label': "Seed Reuse,Seed Purchased,Free Seed",
        'x_label': "Year",
        'colors': TIME_SERIES_COLORS,
        'title': "Percentage of Farmers using Purchased, Reused or Free Seed",
        'confidence': 'High',
        "description":
            "DATASOURCE<br />"
            "Living Standard Measurement Study (LSMS)<br />"
            "2010 Post Planting Agriculture Survey (Section 11e)<br />"
            "2012 Post Planting Agriculture Survey (Section 11e)<br />",
    }

    def update_args_for_valuechain(self, args, valuechain):
        VALUECHAIN_LOOKUP = {
            'cassava': "Cassava%20Old",
            'rice': 'Rice',
        }
        args.update({
            "dataset": "59dd9374b8fe11e4882906909bee25eb",
            "dataset_id": "54e72c9ba750b363fa339a8e",
            'filters': [("Crop", VALUECHAIN_LOOKUP[valuechain])],
        })
        args['title'] += " ({0} Farmers Only, Nationwide)".format(valuechain.capitalize())


class ProductivityPreATAChart(Chart):
    static_args = {
        "dataset": "8ba9c30ca16e11e4927006909bee25eb",
        "dataset_id": "54bfa4b9a750b3418651e0fc",
        'indicators': ["Production", "Yield Per Hectare"],
        'operation': "sum",
        'secondary_operation': "avg",
        'chart_type': "column",
        'y0_label': "Total Production (metric tonnes)",
        'y1_label': "Average Yield (metric tonnes/hectare)",
        'colors': PRE_ATA_COLORS,
        'confidence': 'Medium',
        "description":
            "Datasource<br />"
            "Annual Abstract of Statistics, 2012<br />"
            "National Bureau of Statistics<br />"
            "Primary Data<br />"
            "300,000 Data Points",
    }

    def update_args_for_state(self, args, state):
        self.update_args_for_general_chart(args)
        args['title'] += " (Data cannot be filtered by {0})".format(state.capitalize())

    def update_args_for_valuechain(self, args, valuechain):
        args.update({
            'variables': ["Year"],
            'x_label': "Year",
            'title': "{0} Production and Yield Pre ATA (Nationwide)".
                     format(valuechain.capitalize()),
            'filters': [('Crop', valuechain.capitalize())]
        })

    def update_args_for_see_all(self, args):
        self.update_args_for_general_chart(args)
        args['title'] += " (Nationwide)"

    def update_args_for_general_chart(self, args):
        args.update({
            'variables': ["Crop"],
            'title': "Crop Production and Yield Pre ATA",
            'x_label': "Crop",
            'filters': [('Year', 2009)],
        })


class ProductivityDuringATAChart(Chart):
    static_args = {
        "dataset": "b7b71862b6b511e4882906909bee25eb",
        "dataset_id": "54e35790a750b363fa31fb40",
        'variables': ["Season"],
        'indicators': ["Production", "Yield"],
        'operation': "sum",
        'secondary_operation': "avg",
        'chart_type': "column",
        'y0_label': "Total Production (metric tonnes)",
        'y1_label': "Average Yield (metric tonnes/hectare)",
        'x_label': "Season and Year",
        'title': "Rice Production and Yield During ATA",
        'colors': DURING_ATA_COLORS,
        'confidence': 'Low',
        "description":
            "Datasource<br />"
            "ATA Briefing to the Honorable Minister of Agriculture<br />"
            "Based on Cellulant data from the GES<br />"
            "Secondary Data<br />"
            "1.5M to 8M Farmer Data on Input Redemption",
    }

    def update_args_for_valuechain(self, args, valuechain):
        if valuechain != 'rice':
            args['not_available_message'] = \
                "These data are available for Rice only"
            args['title'] = "{0} Production and Yield During ATA (Nationwide)".format(
                            valuechain.capitalize())


class ProductivityMarketPricesChart(Chart):
    static_args = {
        "dataset": "cfe62ffcb0bd11e4a10c06909bee25eb",
        "dataset_id": "54d9542aa750b33be02c1626",
        'variables': ["Month", "Development"],
        'indicators': ["Value"],
        'operation': "sum",
        'secondary_operation': "avg",
        'chart_type': "line",
        'data_labels': "false",
        'y0_label': "Market Value (Naira)",
        'x_label': "Month",
        'title': "Market Prices in Kogi State",
        'colors': MARKET_PRICE_COLORS,
        'confidence': 'Medium',
        "description":
            "Datasource<br />"
            "Kogi State ADP<br />"
            "Primary Data<br />"
            "Unknown Number of Data Points",
    }
    valuechain_filters = {
        'rice': [
            ('Crop', 'Rice (milled)'),
            ('Crop', 'Rice (paddy)'),
        ],
        'cassava': [
            ('Crop', 'Cassava'),
            ('Crop', 'Garri'),
        ]
    }

    def update_args_for_see_all(self, args):
        """ Don't add nationwide to title, as it is Kogi only """
        pass

    def update_args_for_state(self, args, state):
        if state != 'kogi':
            args['not_available_message'] = \
                "These data are available for Kogi only"
            args['title'] = "Market Prices in {0} State".format(state.capitalize())

    def update_args_for_valuechain(self, args, valuechain):
        args['filters'] = self.valuechain_filters[valuechain][:]
        args['title'] += " ({0} Value Chain)".format(valuechain.capitalize())


class PercentSalesDonutChart(Chart):
    static_args = {
        "dataset": "23c646c0ad2611e48f3706909bee25eb",
        "dataset_id": "54d34d49a750b304561f6605",
        "variables": ["Percent Sales"],
        "indicators": ["Percent Sales"],
        "operation": "avg",
        "chart_type": "percentagedonut",
        "legend": None,
        "data_labels": None,
        "title": "Percentage of Crops Sold",
        "show_explore_button": False,
        'colors': PRE_ATA_ONLY_COLORS,
        'confidence': 'High',
        'description':
            "Datasource:<br />"
            "Living Standards Measurement Study: "
            "Post Harvest Agriculture Survey Section "
            "a3, year 2012 and 2010<br />"
            "Primary Data<br />"
            "5000 Households<br />",
    }

    def __init__(self, year):
        self.year = str(year)

    def update_args_generic(self, args):
        args['chart_title'] = self.year
        args['filters'] = [
            ("Year", self.year),
        ]
        if self.year == "2010":
            args.update({
                'colors': PRE_ATA_ONLY_COLORS,
                'height': "300",
                'width': "300",
            })
        else:
            args.update({
                'colors': DURING_ATA_ONLY_COLORS,
                'height': "600",
                'width': "600",
            })

    def update_args_for_state(self, args, state):
        self.update_args_generic(args)
        args['filters'] += [
            ('State', state.capitalize()),
        ]
        args['title'] += " ({0} Only)".format(state.capitalize())

    def update_args_for_valuechain(self, args, valuechain):
        self.update_args_generic(args)
        VALUECHAIN_LOOKUP = {
            'cassava': "Cassava%20Old",
            'rice': 'Rice',
        }
        args['filters'] += [
            ("Crop", VALUECHAIN_LOOKUP[valuechain]),
        ]
        args['title'] += " ({0} Farmers Only, Nationwide)".format(valuechain.capitalize())

    def update_args_for_see_all(self, args):
        self.update_args_generic(args)
        args['title'] += " (Nationwide)"


class AverageHouseholdSalesChart(Chart):
    static_args = {
        "dataset": "c9704b54adf611e4a54c06909bee25eb",
        "dataset_id": "54d4ab51a750b36f06f10a9a",
        "chart_type": "column",
        "operation": "avg",
        "indicators": ["Total Sales"],
        "variables": ["Gender", "Year"],
        'y0_label': "Average Sales per Household (Naira)",
        'x_label': "Gender and Year",
        "title": "Average Household Sales Across Gender and Year",
        'colors': TIME_SERIES_COLORS,
        'confidence': 'High',
        'description':
            "Datasource:<br />"
            "LSMS Post Harvest Agriculture Survey Section "
            "a3, year 2012 and 2010<br />"
            "Primary Data<br />"
            "5000 Households<br />",
    }

    def update_args_for_state(self, args, state):
        args['filters'] = [('State', state.capitalize())]
        args['title'] += " ({0} Only)".format(state.capitalize())

    def update_args_for_valuechain(self, args, valuechain):
        VALUECHAIN_LOOKUP = {
            'cassava': "Cassava%20Old",
            'rice': 'Rice',
        }
        args.update({
            "dataset": "23c646c0ad2611e48f3706909bee25eb",
            "dataset_id": "54d34d49a750b304561f6605",
            'filters': [("Crop", VALUECHAIN_LOOKUP[valuechain])],
        })
        args['title'] += " ({0} Farmers Only, Nationwide)".format(valuechain.capitalize())

    def update_args_for_see_all(self, args):
        args['title'] += " (Nationwide)"

ALL_CHARTS = {
    'nutrition': NutritionChart(),
    'technology': TechnologyChart(),
    'seed_acquisition': SeedAcquisitionChart(),
    'productivity_pre_ata': ProductivityPreATAChart(),
    'productivity_during_ata': ProductivityDuringATAChart(),
    'productivity_market_price': ProductivityMarketPricesChart(),
    'percent_sales_donut_2010': PercentSalesDonutChart(2010),
    'percent_sales_donut_2012': PercentSalesDonutChart(2012),
    'average_household_sales': AverageHouseholdSalesChart(),
}


def get_all_charts(state, valuechain):
    return dict(
        [(key, chart.get_chart(state, valuechain))
         for key, chart in ALL_CHARTS.iteritems()]
    )
