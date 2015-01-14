from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import HomeView, StateFilterView, ChartsView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^state/(?P<state>\w+)/$', StateFilterView.as_view(), name='state_filter'),
    url(r'^charts/$', ChartsView.as_view(), name='charts'),
)
