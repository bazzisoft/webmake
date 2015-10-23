import re
import os
import subprocess
from subprocess import CalledProcessError
from .. import settings


def log(msg, *args, **kwargs):
    """
    Print out a log message.
    """
    if len(args) == 0 and len(kwargs) == 0:
        print(msg)
    else:
        print(msg.format(*args, **kwargs))


def logv(msg, *args, **kwargs):
    """
    Print out a log message, only if verbose mode.
    """
    if settings.VERBOSE:
        log(msg, *args, **kwargs)


class StaticCompilerError(Exception):
    def __init__(self, message, error=None, output=None, source=None):
        super(StaticCompilerError, self).__init__()
        self.message = message
        self.error = error or ''
        self.output = output or ''
        self.source = source or ''

    def __str__(self):
        err = [
            '\nERROR: ',
            self.message,
            '\n\nReceived error:\n',
            self.error,
        ]

        if self.output:
            err.extend(['\n\nOutput:\n', self.output])

        if self.source:
            err.extend(['\n\nSource:\n', self.source])

        return ''.join(err)


def breadth_first_search(get_deps_fn, root_file):
    root_file = os.path.abspath(root_file)
    queue = [root_file]
    deps = [root_file]

    while len(queue) > 0:
        cur_file = queue.pop(0)
        new_deps = get_deps_fn(cur_file)
        queue.extend(new_deps)
        deps.extend(new_deps)

    return deps


def list_matching_files(path, extensions=None, recursive=True, linux_style_paths=False):
    if isinstance(extensions, list):
        extensions = tuple(extensions)

    result = []

    if recursive:
        it = os.walk(path)
    else:
        it = [(path, (), (f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))))]

    for (dir, _, files) in it:
        if extensions:
            files = [f for f in files if f.endswith(extensions)]

        for f in files:
            f = os.path.join(dir, f)
            if linux_style_paths:
                f = f.replace('\\', '/')
            result.append(f)

    return result


def ensure_path_exists(path):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        os.makedirs(path)


def ensure_deleted(*args):
    for file in args:
        try:
            os.unlink(file)
        except Exception:  # pylint: disable=broad-except
            pass


def rename(old, new):
    ensure_deleted(new)
    os.rename(old, new)


def get_node_modules_dir(module=None):
    moduledir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'node_modules'))
    if module:
        return os.path.join(moduledir, module)
    else:
        return moduledir


def get_node_bin_dir(cmd=None):
    bindir = get_node_modules_dir('.bin')
    if cmd:
        return os.path.join(bindir, cmd)
    else:
        return bindir


def no_dependencies(input):
    if not isinstance(input, (list, tuple)):
        input = [input]
    else:
        return input


def run_command(cmd, errmsg, env=None):
    if env is not None:
        newenv = os.environ.copy()
        newenv.update(env)
        env = newenv

    if isinstance(cmd, (list, tuple)):
        cmd = ' '.join(c for c in cmd if c != '')

    try:
        logv('>>> ' + cmd)
        return subprocess.check_output(cmd, env=env, stderr=subprocess.STDOUT, shell=True).decode('ascii', 'replace')
    except CalledProcessError as e:
        raise StaticCompilerError(errmsg, str(e), e.output.decode('ascii', 'replace'))


def extract_line_num(output, regexp):
    m = re.search(regexp, output)
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            pass
    return None


def extract_lines_from_source(source, line_num):
    start = max(0, line_num - 5)
    with open(source, 'r') as f:
        lines = f.readlines()[start:start + 10]

    ret = ['{}: {}'.format(i + start + 1, l) for (i, l) in enumerate(lines)]
    ret[3] = ret[3].rstrip() + '      <<<<<<\n'
    return ''.join(ret)


