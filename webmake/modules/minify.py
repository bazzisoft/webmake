import os
from . import utils, concat


def minify_js(input_files, output_file, release=False):
    assert isinstance(input_files, (list, tuple))

    if not release:
        concat.concatenate_input_files(input_files, output_file, release=release)
        return

    if output_file:
        utils.ensure_path_exists(os.path.dirname(output_file))

    cmdline = [
        utils.get_node_bin_path('uglify-js', 'bin', 'uglifyjs'),
        '--compress',
        '--mangle',
        '-o',
        output_file,
        '--',
    ]
    cmdline.extend(input_files)

    try:
        utils.run_command(cmdline, 'Failed to minify JS to "{}"'.format(output_file))
    except:
        utils.ensure_deleted(output_file)
        raise


def minify_css(input_files, output_file, release=False):
    assert isinstance(input_files, (list, tuple))

    concat.concatenate_input_files(input_files, output_file, release=release)
    if not release:
        return

    cmdline = [
        utils.get_node_bin_path('clean-css-cli', 'bin', 'cleancss'),
        '--output',
        output_file,
        output_file,
    ]

    try:
        utils.run_command(cmdline, 'Failed to minify CSS to "{}"'.format(output_file))
    except:
        utils.ensure_deleted(output_file)
        raise
