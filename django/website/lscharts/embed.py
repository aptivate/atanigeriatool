from __future__ import unicode_literals, absolute_import

from django.utils.html import escape, mark_safe


class EmbedChartSettings(object):

    def __init__(self, **kwargs):
        self.html_class = kwargs.get("html_class", "insight-tile")
        self.width = kwargs.get("width", "600")
        self.height = kwargs.get("height", "600")
        self.background = kwargs.get("background", "false")
        self.colors = kwargs.get(
            "colors",
            "#0066b3,#00aaad,#00a65d,#72bf44,#fff200,#faa61a,#f58220,#ef413d,#ed1c24,#a3238e,#5c2d91,#214009")

        self.enable_filtering = kwargs.get("enable_filtering", "true")
        self.enable_interaction = kwargs.get("enable_interaction", "true")

        self.domain = kwargs.get("domain", "insight.livestories.com")
        self.dataset = kwargs.get("dataset", "5b19fd0a92bf11e4acc406909bee25eb")
        self.variables = kwargs.get("variables", "Crop")
        self.indicators = kwargs.get("indicators", "__entry")
        self.operation = kwargs.get("operation", "count")
        self.chart_type = kwargs.get("chart_type", "pie")
        if 'filters' in kwargs:
            self.filters = self.format_filters(kwargs["filters"])

        self.text = kwargs.get("text", "Crop")

        self.show_dataset = kwargs.get("show_dataset", "false")
        self.data_labels = kwargs.get("data_labels", "false")
        self.legend = kwargs.get("legend", "false")

    def format_filters(self, filter_list):
        # this is an unsafe string that django will do html escaping on
        formatted = '&'.join(['filters.Term=' + term for term in filter_list])
        formatted = escape(formatted)
        return mark_safe(formatted.replace(' ', '%20'))
