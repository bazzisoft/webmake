import os
import re
from . import utils


SASS_IMPORT_RE = re.compile(r"""@import\s+['"](.+?(?:\.s[ca]ss)?)['"]\s*;""")


def _read_sass_imports(file):
    deps = []
    with open(file) as f:
        sassfile = f.read()
    imports = SASS_IMPORT_RE.findall(sassfile)
    sass_dir = os.path.dirname(file)

    for imp in imports:
        dep = utils.resolve_possible_paths(imp, sass_dir, ['.scss', '.sass', '.css'],
                                           leading_underscore=True)
        if dep:
            deps.append(dep)
        else:
            raise ValueError('Invalid SASS import in {}: {}'.format(file, imp))

    return deps


def sass_dependencies(input_file):
    return utils.breadth_first_search(_read_sass_imports, input_file)


def sass_compile(input_file, output_file, release=False):
    map_file = output_file + '.map'
    output_style = 'compressed' if release else 'expanded'
    if release:
        source_map = '--no-source-map'
    else:
        source_map = '--source-map'

    cmdline = [
        utils.get_node_bin_path('sass', 'sass'),
        '--style',
        output_style,
        '--quiet',
        source_map,
        input_file,
        output_file,
    ]

    try:
        utils.ensure_deleted(map_file)
        utils.run_command(cmdline, 'Failed to compile SASS to "{}"'.format(output_file))
    except:
        utils.ensure_deleted(output_file)
        utils.ensure_deleted(map_file)
        raise
