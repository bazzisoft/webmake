import os
from . import utils


def _trimpath(path):
    comps = []
    for _ in range(3):
        path, c = os.path.split(path)
        comps.append(c)
    return os.path.join(*reversed(comps)).replace('\\', '/')


def concatenate_input_files(input_files, output_file, release=False):
    assert isinstance(input_files, (list, tuple))

    if len(input_files) == 1 and input_files[0] == output_file:
        return

    for f in input_files:
        assert f != output_file, 'Concatenate input file is same as output.'

    if output_file:
        utils.ensure_path_exists(os.path.dirname(output_file))

    try:
        utils.logv('>>> concat {} > {}'.format(' '.join(input_files), output_file))
        with open(output_file, 'w') as output:
            for input_file in input_files:
                with open(input_file, 'r') as input:
                    output.write(input.read())

                if not release:
                    path = _trimpath(input_file)
                    output.write('\n\n'
                                 '/*\n'
                                 ' * {caret}\n'
                                 ' * {path} \n'
                                 ' * {caret}\n'
                                 ' */\n\n\n'.format(path=path, caret='^' * len(path)))

    except IOError as e:
        utils.ensure_deleted(output_file)
        raise utils.StaticCompilerError('Failed to concatenate to {}'.format(output_file), error=str(e))
