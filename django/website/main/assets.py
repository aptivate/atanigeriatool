from __future__ import unicode_literals, absolute_import

from django_assets import Bundle, register

common_css = Bundle(
    'bower_components/bootstrap/less/bootstrap_modified.less',
    'bower_components/bootstrap-material-design/less/material.less',
    'less/main.less',
    filters='less,cssmin',
    output='css/main/common.min.css',
)
register('main.common_css', common_css)

common_js = Bundle(
    # 'bootstrap/ie_version.js',
    'bower_components/jquery/dist/jquery.js',
    'bower_components/bootstrap/dist/js/bootstrap.js',
    # 'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
    'bower_components/bootstrap-material-design/dist/js/material.js',
    filters='jsmin',
    output='js/main/common.min.js'
)
register('main.common_js', common_js)
