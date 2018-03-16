import os
from . import utils, minify


def get_extensions_and_params(use_reactjs=False):
    extensions = ['.js']
    params = []

    if use_reactjs:
        reactify = utils.get_node_modules_dir('reactify')
        extensions.extend(['.jsx'])
        params.extend(['-t', '[', reactify, '--extension', 'jsx', ']', '--extension=.jsx'])

    return (extensions, params)


def browserify_basic_error(func_name, output_file, list_deps):
    if list_deps:
        return 'Failed to list dependencies in {}()'.format(func_name)
    else:
        return 'Error compiling with {}() to "{}"'.format(func_name, output_file)


def browserify_basic_command(output_file, release, list_deps):
    sourcemap = '-d' if not release else ''

    cmdline = [
        utils.get_node_bin_dir('browserify'),
    ]

    if list_deps:
        cmdline.extend([
            '--list',
            '--fast',
        ])
    else:
        cmdline.extend([
            sourcemap,
            '-o',
            output_file,
        ])

    return cmdline


def browserify_run(cmdline, errmsg, output_file, release, list_deps):
    env = {'NODE_ENV': 'production'} if release else None

    try:
        if output_file:
            utils.ensure_path_exists(os.path.dirname(output_file))

        output = utils.run_command(cmdline, errmsg, env=env)
        if list_deps:
            return [os.path.abspath(p) for p in output.splitlines()]
        elif release:
            minify.minify_js([output_file], output_file, release=release)
    except:
        if output_file:
            utils.ensure_deleted(output_file)
        raise


def browserify_node_modules(module_list, output_file=None, release=False, list_deps=False):
    errmsg = browserify_basic_error('browserify_node_modules', output_file, list_deps)
    # No source maps for vendor libs, load time is too slow
    cmdline = browserify_basic_command(output_file, release=True, list_deps=list_deps)

    for m in module_list:
        if m.startswith('./'):
            cmdline.extend(['-r', m + ':' + os.path.basename(m).rsplit('.', maxsplit=1)[0]])
        else:
            cmdline.extend(['-r', m])

    return browserify_run(cmdline, errmsg, output_file, release, list_deps)


def browserify_libs(lib_dirs, output_file=None, release=False, list_deps=False, use_reactjs=False):
    (exts, params) = get_extensions_and_params(use_reactjs=use_reactjs)
    errmsg = browserify_basic_error('browserify_libs', output_file, list_deps)

    cmdline = browserify_basic_command(output_file, release, list_deps)
    cmdline.append('--no-bundle-external')
    cmdline.extend(params)

    for dir in lib_dirs:
        files = utils.list_matching_files(dir, extensions=exts, recursive=True, linux_style_paths=True)
        dir = dir.replace('\\', '/')
        libname = os.path.basename(dir.rstrip('/\\'))

        for f in files:
            assert f.startswith(dir)
            newname = libname + os.path.splitext(f[len(dir):])[0]
            if not os.path.isabs(f):
                f = './' + f
            cmdline.extend(['-r', '{}:{}'.format(f, newname)])

    return browserify_run(cmdline, errmsg, output_file, release, list_deps)


def browserify_file(entry_point, output_file=None, release=False, list_deps=False, use_reactjs=False, export_as=None):
    (_, params) = get_extensions_and_params(use_reactjs=use_reactjs)
    errmsg = browserify_basic_error('browserify_file', output_file, list_deps)

    cmdline = browserify_basic_command(output_file, release, list_deps)
    cmdline.append('--no-bundle-external')
    cmdline.extend(params)

    if not export_as:
        cmdline.extend([
            '-e',
            entry_point,
        ])
    else:
        f = entry_point.replace('\\', '/')
        if not os.path.isabs(f):
            f = './' + f

        cmdline.extend([
            '-r',
            '{}:{}'.format(f, export_as)
        ])

    return browserify_run(cmdline, errmsg, output_file, release, list_deps)


def browserify_deps_node_modules(module_list):
    return browserify_node_modules(module_list, list_deps=True)


def browserify_compile_node_modules(module_list, output_file, release=False):
    browserify_node_modules(module_list, output_file, release=release)


def browserify_deps_libs(lib_dirs, use_reactjs=False):
    return browserify_libs(lib_dirs, list_deps=True, use_reactjs=use_reactjs)


def browserify_compile_libs(lib_dirs, output_file, release=False, use_reactjs=False):
    browserify_libs(lib_dirs, output_file, release=release, use_reactjs=use_reactjs)


def browserify_deps_file(entry_point, use_reactjs=False, export_as=None):
    return browserify_file(entry_point, list_deps=True, use_reactjs=use_reactjs, export_as=export_as)


def browserify_compile_file(entry_point, output_file, release=False, use_reactjs=False, export_as=None):
    browserify_file(entry_point, output_file, release=release, use_reactjs=use_reactjs, export_as=export_as)
