from . import utils, concat


def minify_js(input_files, output_file, release=False):
    assert isinstance(input_files, (list, tuple))

    if not release:
        concat.concatenate_input_files(input_files, output_file, release=release)
        return

    cmdline = [
        utils.get_node_bin_dir('uglifyjs'),
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

    if not release:
        concat.concatenate_input_files(input_files, output_file, release=release)
        return

    cmdline = [
        utils.get_node_bin_dir('cssmin'),
    ]
    cmdline.extend(input_files)

    try:
        output = utils.run_command(cmdline, 'Failed to minify CSS to "{}"'.format(output_file))
    except:
        utils.ensure_deleted(output_file)
        raise

    try:
        with open(output_file, 'w') as f:
            f.write(output)
    except IOError as e:
        utils.ensure_deleted(output_file)
        raise utils.StaticCompilerError('Failed to minify CSS to "{}"'.format(output_file), str(e))
