from webmake import api


NODE_MODULES = [
    'jquery',
    'underscore',
    'bootstrap',
    'fastclick',
    'react',
]


JSX_INPUTS = api.list_matching_files('www-dev/jsx', extensions='jsx', recursive=False)


MAKEFILE = [
    # Copy static assets
    api.copy_files('www-dev', 'www', 'index.html'),
    api.copy_files('node_modules/bootstrap/fonts', 'www/fonts'),

    # Compile LESS
    api.compile_less('www-dev/less/base.less', 'www/css/base.css'),

    # Broserify vendor javascript libs from node_modules
    api.browserify_node_modules(NODE_MODULES, 'www/js/vendor.js'),

    # Browserify user libs
    # Usage: var Cookie = require('jslib/Cookie');
    api.browserify_libs(['www-dev/jslib'], 'www/js/jslib.js', use_reactjs=False),

    # Browserify an entry point that require()'s all its dependencies
    # Use export_as=xxx to expose it as a require()'able module named xxx
    api.browserify_file('www-dev/js/website.js', 'www/js/website.js', use_reactjs=False, export_as=None),

    # Concatenate and compile standalone JSX files with react-tools.
    # If using browserify, use above APIs instead with use_reactjs=True
    api.compile_reactjsx(JSX_INPUTS, 'www/js/reactjsx.js'),

    # Minify standalone CSS. Concatenates in debug mode, minifies in release mode.
    api.minify_css(['www-dev/less/styles.css'], 'www/css/styles.css'),

    # Minify standalone JS. Concatenates in debug mode, minifies in release mode.
    api.minify_js(['www-dev/js/standalone.js'], 'www/js/standalone.js'),

    # Concatenate standalone files with no further processing.
    api.concatenate(['www-dev/js/standalone.js'] * 2, 'www/js/standalone-x2.js'),
]
