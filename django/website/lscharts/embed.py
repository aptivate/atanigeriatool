from __future__ import unicode_literals, absolute_import

from urllib import urlencode

from django.utils.html import escape, mark_safe

DEFAULT_DESCRIPTION = \
    "Scotch ale lambic, hoppy ester double bock/dopplebock. brewpub " \
    "units of bitterness amber copper grainy specific gravity. mouthfeel " \
    "bunghole mash double bock/dopplebock, infusion hydrometer, \" real " \
    "ale brewhouse.\" lager, copper brewpub goblet scotch ale all-malt " \
    "length pint glass, carbonation cold filter. "

DEFAULT_COLORS = [
    "7a7654",
    "1d976b",
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
        self.not_available_message = kwargs.get(
            "not_available_message",
            None
        )
        self.html_class = kwargs.get("html_class", "insight-tile")
        self.width = kwargs.get("width", "600")
        self.height = kwargs.get("height", "600")
        self.background = kwargs.get("background", "true")
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
        self.category_order = kwargs.get("category_order", "alphabetical")
        self.filters = kwargs.get("filters", None)

        self.title = kwargs.get("title", "Crop")
        self.show_title = kwargs.get("show_title", "false")
        self.description = kwargs.get("description", DEFAULT_DESCRIPTION)

        self.show_dataset = kwargs.get("show_dataset", "false")
        self.data_labels = kwargs.get("data_labels", "true")
        self.legend = kwargs.get("legend", "true")
        self.grid_lines = kwargs.get("grid_lines", "false")
        self.precision = kwargs.get("precision", 0)

    def filters_for_embed_link(self):
        if self.filters is None:
            return ''
        # this is an unsafe string that django will do html escaping on
        formatted = '&'.join(['filters.%s=%s' % (term[0], term[1]) for term in self.filters])
        formatted = escape(formatted)
        return mark_safe(formatted.replace(' ', '%20'))

    def _iterable_comma(self, iterable):
        return ','.join(iterable)

    def variables_comma(self):
        return self._iterable_comma(self.variables)

    def indicators_comma(self):
        return self._iterable_comma(self.indicators)

    def colors_comma(self):
        return self._iterable_comma(['#' + c for c in self.colors])

    def _get_query_params(self):
        query_params = {
            'datasetId': self.dataset_id,
            'dashId': '',
            'dashboard': '',
            'chartType': self.chart_type,
            'operation': self.operation,
            'title': self.title,
            'variables': self.variables,
            'indicators': self.indicators,
            'colors': self.colors,
        }
        if self.secondary_operation:
            query_params['secondaryOperation'] = self.secondary_operation
        if self.category_order:
            query_params['categoryOrder'] = self.category_order
        return query_params

    def explore_url(self):
        """should return something like

        http://ata.livestories.com/guest/chart?variables=season
            & colors=1d976b
            & colors=7a7654
            ...
            & colors=214009
            & dashboard=
            & title=Total+production+and+average+of+yield+across+season+%28cassava+value+chain%29
            & indicators=production
            & indicators=yield
            & chartType=column
            & operation=sum
            & dashId=
            & datasetId=54be3923a750b3418651e0d9
            & secondaryOperation=avg

        (without the whitespace)
        """
        link = "http://ata.livestories.com/guest/chart?"
        link += urlencode(self._get_query_params(), doseq=True)
        filter_part = self.filters_for_embed_link()
        if filter_part:
            link += '&' + filter_part
        return mark_safe(link)
