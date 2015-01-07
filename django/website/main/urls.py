from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import ChartsView

urlpatterns = patterns(
    '',
    url(r'^charts/$', ChartsView.as_view(), name='charts'),
)
