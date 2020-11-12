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
    input_abs = os.path.abspath(os.path.dirname(input_file))
    output_abs = os.path.abspath(os.path.dirname(output_file))
    map_url = os.path.basename(map_file)
    map_base = os.path.commonprefix([input_abs, output_abs]).replace('\\', '/')
    map_rel = os.path.dirname(output_abs[len(map_base):]).replace('\\', '/')
    map_root = '/'.join([os.pardir] * len(map_rel.split('/')))

    minify = '-x' if release else ''
    sourcemap = ('-source-map-rootpath={rp} --source-map-basepath={bp} --source-map-url={url} --source-map={map}'
                 .format(rp=map_root, bp=map_base, url=map_url, map=map_file)
                 if not release else '')

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
