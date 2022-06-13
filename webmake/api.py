

def list_matching_files(dir, extensions=None, recursive=True):
    """
    Returns a list of all files in the specified directory,
    optionally recursively and/or with the specified extensions.
    """
    from .modules import utils
    return utils.list_matching_files(dir, extensions=extensions, recursive=recursive)


def concatenate(input_files, output_file):
    """
    Concatenates the input files into the single output file.

    In debug mode this function adds a comment with the filename
    before the contents of each file.
    """
    from .modules import utils, concat

    if not isinstance(input_files, (list, tuple)):
        raise RuntimeError('Concatenate takes a list of input files.')

    return {
        'dependencies_fn': utils.no_dependencies,
        'compiler_fn': concat.concatenate_input_files,
        'input': input_files,
        'output': output_file,
        'kwargs': {},
    }


def copy_files(src_dir, dst_dir, filespec='*', recursive=False):
    """
    Copies any files matching filespec from src_dir into dst_dir.

    If `recursive` is `True`, also copies any matching directories.
    """
    import os
    from .modules import copyfiles

    if src_dir == dst_dir:
        raise RuntimeError('copy_files() src and dst directories must be different.')

    if not os.path.isdir(src_dir):
        raise RuntimeError('copy_files() src directory "{}" does not exist.'.format(src_dir))

    return {
        'dependencies_fn': copyfiles.list_files,
        'compiler_fn': copyfiles.copy_files,
        'input': src_dir,
        'output': dst_dir,
        'kwargs': {
            'filespec': filespec,
            'recursive': recursive,
        },
    }


def minify_js(input_files, output_file):
    """
    Minifies the input javascript files to the output file.

    Output file may be same as input to minify in place.

    In debug mode this function just concatenates the files
    without minifying.
    """
    from .modules import minify, utils

    if not isinstance(input_files, (list, tuple)):
        raise RuntimeError('JS minifier takes a list of input files.')

    return {
        'dependencies_fn': utils.no_dependencies,
        'compiler_fn': minify.minify_js,
        'input': input_files,
        'output': output_file,
        'kwargs': {},
    }


def minify_css(input_files, output_file):
    """
    Minifies the input CSS files to the output file.

    Output file may be same as input to minify in place.

    In debug mode this function just concatenates the files
    without minifying.
    """
    from .modules import minify, utils

    if not isinstance(input_files, (list, tuple)):
        raise RuntimeError('CSS minifier takes a list of input files.')

    return {
        'dependencies_fn': utils.no_dependencies,
        'compiler_fn': minify.minify_css,
        'input': input_files,
        'output': output_file,
        'kwargs': {},
    }


def compile_less(input_file, output_file):
    """
    Compile a LESS source file. Minifies the output in release mode.
    """
    from .modules import less

    if not isinstance(input_file, str):
        raise RuntimeError('LESS compiler takes only a single input file.')

    return {
        'dependencies_fn': less.less_dependencies,
        'compiler_fn': less.less_compile,
        'input': input_file,
        'output': output_file,
        'kwargs': {},
    }


def compile_sass(input_file, output_file):
    """
    Compile a SASS source file. Minifies the output in release mode.
    """
    from .modules import sass

    if not isinstance(input_file, str):
        raise RuntimeError('SASS compiler takes only a single input file.')

    return {
        'dependencies_fn': sass.sass_dependencies,
        'compiler_fn': sass.sass_compile,
        'input': input_file,
        'output': output_file,
        'kwargs': {},
    }


def browserify_node_modules(module_name_list, output_file, babelify=False):
    """
    Browserify a list of libraries from node_modules into a single
    javascript file. Generates source maps in debug mode. Minifies the
    output in release mode.

    Note you may also specify the relative path to the module
    as ``./path/to/module`` or ``./path/to/module/file.js``.
    """
    from .modules import browserify

    if not isinstance(module_name_list, (list, tuple)):
        raise RuntimeError('Browserify Node Modules compiler takes a list of node module names as input.')

    return {
        'dependencies_fn': browserify.browserify_deps_node_modules,
        'compiler_fn': browserify.browserify_compile_node_modules,
        'input': module_name_list,
        'output': output_file,
        'kwargs': {
            'babelify': babelify,
        },
    }


def browserify_libs(lib_dirs, output_file, babelify=False):
    """
    Browserify one or more library directories into a single
    javascript file. Generates source maps in debug mode. Minifies the
    output in release mode.

    The final directory name in each of lib_dirs is the library name
    for importing. Eg.::

        lib_dirs = ['cordova_libs/jskit']

        var MyClass = require('jskit/MyClass');
    """
    from .modules import browserify

    if not isinstance(lib_dirs, (list, tuple)):
        raise RuntimeError('Browserify Libs compiler takes a list of library directories as input.')

    return {
        'dependencies_fn': browserify.browserify_deps_libs,
        'compiler_fn': browserify.browserify_compile_libs,
        'input': lib_dirs,
        'output': output_file,
        'kwargs': {
            'babelify': babelify,
        },
    }


def browserify_file(entry_point, output_file, babelify=False, export_as=None):
    """
    Browserify a single javascript entry point plus non-external
    dependencies into a single javascript file. Generates source maps
    in debug mode. Minifies the output in release mode.

    By default, it is not possible to ``require()`` any exports from the entry
    point or included files. If ``export_as`` is specified, any module exports
    in the specified entry point are exposed for ``require()`` with the
    name specified by ``export_as``.
    """
    from .modules import browserify

    if not isinstance(entry_point, str):
        raise RuntimeError('Browserify File compiler takes a single entry point as input.')

    return {
        'dependencies_fn': browserify.browserify_deps_file,
        'compiler_fn': browserify.browserify_compile_file,
        'input': entry_point,
        'output': output_file,
        'kwargs': {
            'babelify': babelify,
            'export_as': export_as,
        },
    }


def custom_function(func, input_files, output_file):
    """
    Calls a custom function which must create the output file.

    The custom function takes 3 parameters: ``input_files``,
    ``output_file`` and a boolean ``release``.
    """
    from .modules import utils

    return {
        'dependencies_fn': utils.no_dependencies,
        'compiler_fn': func,
        'input': input_files,
        'output': output_file,
        'kwargs': {},
    }
