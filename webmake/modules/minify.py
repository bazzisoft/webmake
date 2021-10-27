import os
from . import utils, concat


def minify_js(input_files, output_file, release=False, annotate_angular=False):
    assert isinstance(input_files, (list, tuple))

    if not release:
        concat.concatenate_input_files(input_files, output_file, release=release)
        return

    if annotate_angular:
        # Rather than annotate several individual files (and having to creating temp files as well), it's
        # easier to just concatenate the input_files right now, and then perform the annotation upon that
        # one file. We must then update the `input_files` value accordingly, so that it gets passed into
        # uglify correctly.
        concat.concatenate_input_files(input_files, output_file, release=release)
        input_files = [output_file]
        try:
            annotate_angular_injections(output_file, output_file)
        except:
            utils.ensure_deleted(output_file)
            raise

    if output_file:
        utils.ensure_path_exists(os.path.dirname(output_file))

    cmdline = [
        utils.get_node_bin_path('uglify-es', 'bin', 'uglifyjs'),
        '--compress',
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

def annotate_angular_injections(input_file, output_file):
    cmdline = [
        os.path.join(utils.get_node_bin_path('ng-annotate'), 'ng-annotate.js'),
        '--add',
        '-o',
        output_file,
    ]
    cmdline.extend([input_file])

    try:
        utils.run_command(cmdline, 'Failed to annotate Angular injections to "{}"'.format(output_file), with_node=True)
    except Exception as e:
        utils.ensure_deleted(output_file)
        raise

def minify_css(input_files, output_file, release=False):
    assert isinstance(input_files, (list, tuple))

    concat.concatenate_input_files(input_files, output_file, release=release)
    if not release:
        return

    cmdline = [
        utils.get_node_bin_path('cssmin', 'bin', 'cssmin'),
    ]
    cmdline.append(output_file)

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
