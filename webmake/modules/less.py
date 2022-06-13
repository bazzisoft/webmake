import os
import re
from . import utils


LESS_IMPORT_RE = re.compile(r"""@import\s+['"](.+?(?:\.less)?)['"]\s*;""")


def _read_less_imports(file):
    deps = []
    with open(file) as f:
        less = f.read()
    imports = LESS_IMPORT_RE.findall(less)
    less_dir = os.path.dirname(file)

    for imp in imports:
        dep = utils.resolve_possible_paths(imp, less_dir, ['.less'])
        if dep:
            deps.append(dep)
        else:
            raise ValueError('Invalid LESS import in {}: {}'.format(file, imp))

    return deps


def less_dependencies(input_file):
    return utils.breadth_first_search(_read_less_imports, input_file)


def less_compile(input_file, output_file, release=False):
    map_file = output_file + '.map'
    map_url = os.path.basename(map_file)

    minify = '-x' if release else ''
    if release:
        sourcemap = ''
    else:
        sourcemap = '--source-map-url={url} --source-map={map}'.format(url=map_url, map=map_file)

    cmdline = [
        utils.get_node_bin_path('less', 'bin', 'lessc'),
        '--no-color',
        minify,
        sourcemap,
        input_file,
        output_file,
    ]

    try:
        utils.ensure_deleted(map_file)
        utils.run_command(cmdline, 'Failed to compile LESS to "{}"'.format(output_file))
    except:
        utils.ensure_deleted(output_file)
        utils.ensure_deleted(map_file)
        raise
