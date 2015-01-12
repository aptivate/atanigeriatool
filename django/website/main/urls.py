from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import HomeView, ChartsView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^charts/$', ChartsView.as_view(), name='charts'),
)
