from __future__ import unicode_literals, absolute_import

from django.utils.html import escape, mark_safe

DEFAULT_DESCRIPTION = \
    "Scotch ale lambic, hoppy ester double bock/dopplebock. brewpub " \
    "units of bitterness amber copper grainy specific gravity. mouthfeel " \
    "bunghole mash double bock/dopplebock, infusion hydrometer, \" real " \
    "ale brewhouse.\" lager, copper brewpub goblet scotch ale all-malt " \
    "length pint glass, carbonation cold filter. "

DEFAULT_COLORS = [
    "1d976b",
    "7a7654",
    "00a65d",
    "72bf44",
    "fff200",
    "faa61a",
    "f58220",
    "ef413d",
    "ed1c24",
    "a3238e",
    "5c2d91",
    "214009"
]


class EmbedChartSettings(object):

    def __init__(self, **kwargs):
        # TODO: could split into chart types with relevant bits in each type
        self.html_class = kwargs.get("html_class", "insight-tile")
        self.width = kwargs.get("width", "600")
        self.height = kwargs.get("height", "600")
        self.background = kwargs.get("background", "false")
        self.colors = kwargs.get("colors", DEFAULT_COLORS)

        self.enable_filtering = kwargs.get("enable_filtering", "true")
        self.enable_interaction = kwargs.get("enable_interaction", "false")

        self.domain = kwargs.get("domain", "insight.livestories.com")
        self.dataset = kwargs.get("dataset", "5b19fd0a92bf11e4acc406909bee25eb")
        self.dataset_id = kwargs.get("dataset_id", "54aff583a750b33915f0069c")
        self.variables = kwargs.get("variables", ["Crop"])
        self.indicators = kwargs.get("indicators", ["__entry"])
        self.operation = kwargs.get("operation", "count")
        self.secondary_operation = kwargs.get("secondary_operation", None)
        self.chart_type = kwargs.get("chart_type", "pie")
        if 'filters' in kwargs:
            self.filters = self.format_filters(kwargs["filters"])

        self.text = kwargs.get("text", "Crop")
        self.description = kwargs.get("description", DEFAULT_DESCRIPTION)

        self.show_dataset = kwargs.get("show_dataset", "false")
        self.data_labels = kwargs.get("data_labels", "false")
        self.legend = kwargs.get("legend", "false")
        self.grid_lines = kwargs.get("grid_lines", "false")
        self.precision = kwargs.get("precision", 0)

    def format_filters(self, filter_list):
        # this is an unsafe string that django will do html escaping on
        formatted = '&'.join(['filters.%s=%s' % (term[0], term[1]) for term in filter_list])
        formatted = escape(formatted)
        return mark_safe(formatted.replace(' ', '%20'))

    def _iterable_comma(self, iterable):
        return ','.join(iterable)

    def _iterable_url_args(self, iterable, url_key):
        return '&'.join([url_key + '=' + i for i in iterable])

    def variables_comma(self):
        return self._iterable_comma(self.variables)

    def variables_url_args(self):
        return self._iterable_url_args(self.variables, 'variables')

    def indicators_comma(self):
        return self._iterable_comma(self.indicators)

    def indicators_url_args(self):
        return self._iterable_url_args(self.indicators, 'indicators')

    def colors_comma(self):
        return self._iterable_comma(['#' + c for c in self.colors])

    def colors_url_args(self):
        return self._iterable_url_args(self.colors, 'colors')
