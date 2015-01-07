from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView


# NOT included in main/urls.py - included directly in the root urls.py
class HomeView(TemplateView):
    template_name = 'main/homepage.html'
