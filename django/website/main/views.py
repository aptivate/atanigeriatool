from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView

from .charts import get_all_charts


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

    def get_charts(self, state, valuechain):
        return get_all_charts(state, valuechain)
