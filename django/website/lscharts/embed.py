from __future__ import unicode_literals, absolute_import


class EmbedChartSettings(object):

    def __init__(self, **kwargs):
        self.html_class = kwargs.get("html_class", "insight-tile")
        self.width = kwargs.get("width", "600")
        self.height = kwargs.get("height", "600")
        self.enable_filtering = kwargs.get("enable_filtering", "true")
        self.dataset = kwargs.get("dataset", "5b19fd0a92bf11e4acc406909bee25eb")
        self.variables = kwargs.get("variables", "Crop")
        self.indicators = kwargs.get("indicators", "__entry")
        self.operation = kwargs.get("operation", "count")
        self.chart_type = kwargs.get("chart_type", "pie")
        self.colors = kwargs.get(
            "colors",
            "#0066b3,#00aaad,#00a65d,#72bf44,#fff200,#faa61a,#f58220,#ef413d,#ed1c24,#a3238e,#5c2d91,#214009")
        self.show_dataset = kwargs.get("show_dataset", "false")
        self.domain = kwargs.get("domain", "insight.livestories.com")
        self.text = "Crop"
