from __future__ import unicode_literals, absolute_import

from django_assets import Bundle, register

common_css = Bundle(
    Bundle(
        # 'bower_components/bootstrap-sass/assets/stylesheets/_bootstrap.scss',
        'sass/bootstrap/bootstrap.scss',
        # 'bower_components/bootstrap-material-design/sass/material.scss',
        'sass/main.scss',
        filters='pyscss',
        output='css/main/from-scss.css',
    ),
    'bower_components/bootstrap-material-design/dist/css/material.css',
    filters='cssmin',
    output='css/main/common.min.css',
)
register('main.common_css', common_css)

common_js = Bundle(
    'bootstrap/ie_version.js',
    'bower_components/jquery/dist/jquery.js',
    'js/bootstrap.js',
    # 'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
    'bower_components/bootstrap-material-design/dist/js/material.js',
    filters='jsmin',
    output='js/main/common.min.js'
)
register('main.common_js', common_js)
