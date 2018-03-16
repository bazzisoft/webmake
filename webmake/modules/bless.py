from . import utils


def bless_css(input_file, output_file, release=False):
    assert isinstance(input_file, str)

    cmdline = [
        utils.get_node_bin_dir('blessc'),
        '--no-imports',
    ]
    cmdline.append(input_file)
    cmdline.append(output_file)

    try:
        utils.run_command(cmdline, 'Failed to split CSS to "{}"'.format(output_file))
    except:
        utils.ensure_deleted(output_file)
        raise
