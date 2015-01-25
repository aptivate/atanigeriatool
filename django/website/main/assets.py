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

print_css = Bundle(
    'less/print.less',
    filters='less,cssmin',
    output='css/main/print.min.css',
)
register('main.print_css', print_css)

common_js = Bundle(
    # 'bootstrap/ie_version.js',
    'bower_components/jquery/dist/jquery.js',
    # 'bower_components/bootstrap/dist/js/bootstrap.js',
    'bower_components/bootstrap/js/affix.js',
    'bower_components/bootstrap/js/collapse.js',
    'bower_components/bootstrap/js/modal.js',
    'bower_components/bootstrap/js/transition.js',
    # 'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
    'bower_components/bootstrap-material-design/scripts/material.js',
    filters='rjsmin',
    output='js/main/common.min.js'
)
register('main.common_js', common_js)
