from __future__ import unicode_literals, absolute_import

from random import randint
from urllib import urlencode

from django.utils.html import conditional_escape, mark_safe

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
        self.html_id = kwargs.get("html_id", "insight-tile-{}".format(randint(1, 100)))
        self.width = kwargs.get("width", "1000")
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
        self.x_label = kwargs.get("x_label", None)
        self.y0_label = kwargs.get("y0_label", None)
        self.y1_label = kwargs.get("y1_label", None)
        self.legend = kwargs.get("legend", "true")
        self.grid_lines = kwargs.get("grid_lines", "true")
        self.precision = kwargs.get("precision", 1)

    def _filter_query_string(self):
        if self.filters is None:
            return ''
        formatted = '&'.join(['filters.%s=%s' % (term[0], term[1]) for term in self.filters])
        return mark_safe(formatted.replace(' ', '%20'))

    def filters_for_embed_link(self):
        formatted = conditional_escape(self._filter_query_string())
        return mark_safe(formatted)

    def _iterable_comma(self, iterable):
        return ','.join(iterable)

    def variables_comma(self):
        return self._iterable_comma(self.variables)

    def indicators_comma(self):
        return self._iterable_comma(self.indicators)

    def colors_comma(self):
        return self._iterable_comma(['#' + c for c in self.colors])

    def _bool_str_to_num(self, attr):
        if getattr(self, attr).lower() == "true":
            return 1
        else:
            return 0

    def _get_iframe_query_params(self):
        query_params = {
            'dataset': self.dataset,
            'chartType': self.chart_type,
            'operation': self.operation,
            'title': self.title,
            'variables': self.variables,
            'indicators': self.indicators,
            'colors': self.colors,
            'precision': self.precision,
            'height': self.height,
            'show-data-labels': self._bool_str_to_num('data_labels'),
            'show-dataset': self._bool_str_to_num('show_dataset'),
            'show-grid-lines': self._bool_str_to_num('grid_lines'),
            'show-legend': self._bool_str_to_num('legend'),
            'show-title': self._bool_str_to_num('show_title'),
            'enable-filtering': self._bool_str_to_num('enable_filtering'),
            'enable-interaction': self._bool_str_to_num('enable_interaction'),
        }
        for attr, param_name in [
            ('secondary_operation', 'secondaryOperation'),
            ('category_order', 'categoryOrder'),
            ('x_label', 'xLabel'),
            ('y0_label', 'y0Label'),
            ('y1_label', 'y1Label'),
        ]:
            if hasattr(self, attr) and getattr(self, attr):
                query_params[param_name] = getattr(self, attr)
        return query_params

    def iframe_url(self):
        """should return something like

        <iframe
        id="inspire-tile-8"
        src="
            //ata.livestories.com/chart/embed?
            dataset=9e3d0cd49d7e11e4a93606909bee25eb
            &amp;amp; variables=Technology
            &amp;amp; variables=year
            &amp;amp; indicators=Value
            &amp;amp; colors=7a7654
            &amp;amp; colors=1d976b
            ...
            &amp;amp; colors=214009
            &amp;amp; operation=avg
            &amp;amp; chartType=column
            &amp;amp; categoryOrder=alphabetical
            &amp;amp; precision=1
            &amp;amp; xLabel=Technology, year
            &amp;amp; y0Label=Percentage of farmers
            &amp;amp; height=600
            &amp;amp; show-data-labels=1
            &amp;amp; show-title=0
            &amp;amp; show-legend=1
            &amp;amp; show-dataset=0
            &amp;amp; enable-filtering=1
            &amp;amp; title=

        Percentage of farmers who use technologies
        "
        style="width: 100%; max-width: 1000px;"
        frameborder="0"
        height="600"
        width="1000">
        </iframe>
        """
        url = '//{}/chart/embed?'.format(self.domain)
        url += urlencode(self._get_iframe_query_params(), doseq=True)
        filter_part = self.filters_for_embed_link()
        if filter_part:
            url += '&' + filter_part
        url = conditional_escape(url)
        # the site does appear to work properly with double escaping!
        # and indeed that is what the embed.js script produces
        return mark_safe(conditional_escape(url))

    def iframe_element(self):
        """should return something like

        <iframe
        id="inspire-tile-8"
        src="<IFRAME URL>"
        style="width: 100%; max-width: 1000px;"
        frameborder="0"
        height="600"
        width="1000">
        </iframe>
        """
        element = ' '.join([
            '<iframe',
            'id="inspire-tile"',
            'src="{}"'.format(self.iframe_url()),
            'style="width: 100%; max-width: {}px;"'.format(self.width),
            'frameborder="0"',
            'height="{}"'.format(self.height),
            'width="{}">'.format(self.width),
            '</iframe>',
        ])
        return mark_safe(element)

    def _get_explore_query_params(self):
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
        link += urlencode(self._get_explore_query_params(), doseq=True)
        filter_part = self.filters_for_embed_link()
        if filter_part:
            link += '&' + filter_part
        return mark_safe(conditional_escape(link))
