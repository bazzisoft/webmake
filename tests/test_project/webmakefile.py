from webmake import api


NODE_MODULES = [
    "jquery",
    "underscore",
    "bootstrap",
    "fastclick",
    "react",
    "react-dom",
]


JSX_INPUTS = api.list_matching_files("www-dev/jsx", extensions="jsx", recursive=False)


def custom_compiler(input_files, output_file, release):
    with open(output_file, "w") as f:
        f.write("DEBUG\n\n" if not release else "RELEASE\n\n")
        f.write("Hello there!")


MAKEFILE = [
    # Copy static assets
    api.copy_files("www-dev", "www", "index.html"),
    api.copy_files("node_modules/bootstrap/fonts", "www/fonts"),
    # Compile LESS
    api.compile_less("www-dev/less/base.less", "www/css/base.css"),
    # Compile SASS/SCSS
    api.compile_sass("www-dev/scss/base.scss", "www/css/base-scss.css"),
    # Broserify vendor javascript libs from node_modules
    api.browserify_node_modules(NODE_MODULES, "www/js/vendor.js", babelify=False),
    # Browserify user libs
    # Usage: var Cookie = require('jslib/Cookie');
    api.browserify_libs(["www-dev/jslib"], "www/js/jslib.js", babelify=False),
    # Browserify an entry point that require()'s all its dependencies
    # Use export_as=xxx to expose it as a require()'able module named xxx
    api.browserify_file(
        "www-dev/js/website.js", "www/js/website.js", babelify=False, export_as=None
    ),
    # Browserify ES6 code with optional React JSX
    api.browserify_file(
        "www-dev/jsx/index.js", "www/js/reactjsx.js", babelify=True, export_as="reactjsx"
    ),
    # Minify standalone CSS. Concatenates in debug mode, minifies in release mode.
    api.minify_css(["www-dev/less/styles.css"], "www/css/styles.css"),
    # Minify standalone JS. Concatenates in debug mode, minifies in release mode.
    api.minify_js(["www-dev/js/standalone.js"], "www/js/standalone.js"),
    # Concatenate standalone files with no further processing.
    api.concatenate(["www-dev/js/standalone.js"] * 2, "www/js/standalone-x2.js"),
    # Run a custom function to create an output file
    api.custom_function(custom_compiler, "www-dev/index.html", "www/custom-compiler.txt"),
]
