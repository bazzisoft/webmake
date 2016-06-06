import os
from . import utils, concat, minify


def jsx_compile(input_files, output_file, release=False):
    utils.ensure_deleted(output_file)

    output_dir = os.path.dirname(output_file)
    output_base = os.path.splitext(os.path.basename(output_file))[0]
    tmp_file = os.path.join(output_dir, output_base + '.tmpjsx')
    concat.concatenate_input_files(input_files, tmp_file, release=release)

    sourcemap = '--source-map-inline' if not release else ''

    cmdline = [
        utils.get_node_bin_path('react-tools', 'bin', 'jsx'),
        '--no-cache-dir',
        sourcemap,
        '--extension',
        'tmpjsx',
        output_dir,
        output_dir,
        output_base,
    ]

    try:
        utils.run_command(cmdline, 'Failed to compile React JSX to "{}"'.format(output_file))
    except:
        utils.ensure_deleted(tmp_file)
        utils.ensure_deleted(output_base + '.js')
        raise

    utils.ensure_deleted(tmp_file)
    generated = os.path.abspath(os.path.join(output_dir, output_base + '.js'))
    output = os.path.abspath(output_file)
    if generated != output:
        utils.rename(generated, output)

    if release:
        minify.minify_js([output_file], output_file, release=release)
