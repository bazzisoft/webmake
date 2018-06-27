import os
import re
import shutil
from fnmatch import fnmatch
from . import utils


def list_files(src_dir, filespec, recursive=False, include_dirs=True):
    inputs = []
    filespecs = [filespec] if not isinstance(filespec, (list, tuple)) else filespec

    def match_file(f):
        return any(fnmatch(f, s) for s in filespecs)

    for dir, _, files in os.walk(src_dir):
        if include_dirs:
            inputs.append(dir)

        inputs.extend(os.path.join(dir, f) for f in files if match_file(f))

        if not recursive:
            break

    return inputs


def copy_files(src_dir, dst_dir, filespec, recursive=False, release=None):
    assert src_dir != dst_dir, 'Source and destination directories are the same.'
    assert os.path.isdir(src_dir), 'Source directory "{}" does not exist.'.format(src_dir)

    if not os.path.isdir(dst_dir):
        try:
            os.mkdir(dst_dir)
        except OSError as e:
            raise utils.StaticCompilerError('Failed to create destination dir "{}"'.format(dst_dir), error=str(e))

    input_files = list_files(src_dir, filespec, recursive, include_dirs=False)
    output_files = [os.path.join(dst_dir, os.path.relpath(p, src_dir)) for p in input_files]

    for input, output in zip(input_files, output_files):
        utils.logv('>>> copy {} > {}'.format(input, output))
        dirname = os.path.split(output)[0]
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        shutil.copy2(input, output)

    os.utime(dst_dir, None)
