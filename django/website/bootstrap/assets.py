from __future__ import unicode_literals, absolute_import

from django_assets import Bundle, register

common_css = Bundle(
    # 'bower_components/bootstrap-sass/assets/stylesheets/_bootstrap.scss',
    'sass/bootstrap/bootstrap.scss',
    # 'bower_components/bootstrap-material-design/sass/material.scss',
    'sass/bootstrap.scss',
    filters='pyscss, cssmin',
    output='css/bootstrap/common.min.css'
)

register('bootstrap.common_css', common_css)

common_js = Bundle(
    'bootstrap/ie_version.js',
    'bower_components/jquery/dist/jquery.js',
    'js/bootstrap.js',
    # 'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
    # 'bower_components/bootstrap-material-design/scripts/material.js',
    filters='jsmin',
    output='js/bootstrap/common.min.js'
)
register('bootstrap.common_js', common_js)
