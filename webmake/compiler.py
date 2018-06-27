import os
import json
from .modules.utils import log, logv, StaticCompilerError


def load_dependencies_for_target(target, makefilepath):
    logv('\nFinding dependencies for: {}'.format(target['output']))
    try:
        dependency_fn = target['dependencies_fn']
        target['dependencies'] = [makefilepath] + dependency_fn(target['input'], **target['kwargs'])
    except (IOError, OSError) as e:
        msg = '\nERROR: Failed loading dependencies for "{}":\n\nReceived error:\n{}'.format(target['output'], str(e))
        log(msg)
        return False
    except StaticCompilerError as e:
        log(str(e))
        return False

    return True


def save_dependencies_to_cache(targets, makefilepath):
    cachefile = makefilepath + '.depscache'
    logv('\nWriting dependencies cache: {}'.format(cachefile))

    cache = [{'output': t['output'], 'dependencies': t['dependencies']}
             for t in targets if 'dependencies' in t]

    with open(cachefile, 'w') as f:
        json.dump(cache, f, indent=4)


def load_dependencies_from_cache(targets, makefilepath):
    cachefile = makefilepath + '.depscache'
    try:
        with open(cachefile, 'r') as f:
            cache = json.load(f)
    except IOError:
        return

    for i, entry in enumerate(cache):
        output = entry['output']
        deps = entry['dependencies']

        if i >= len(targets):
            break

        if targets[i]['output'] == output:
            targets[i]['dependencies'] = deps


def dependencies_are_up_to_date(target):
    output = target['output']
    deps = target.get('dependencies')
    last_compiled_timestamp = os.path.getmtime(output) if os.path.exists(output) else -1

    if not deps:
        return False

    for file in deps:
        try:
            if os.path.getmtime(file) >= last_compiled_timestamp:
                return False
        except Exception:
            return False

    return True


def compile_if_modified(targets, makefilepath, release):
    modified = False
    first_up_to_date = True

    for target in targets:
        if dependencies_are_up_to_date(target):
            if first_up_to_date:
                logv('')
                first_up_to_date = False
            logv('Up-to-date: {}', target['output'])
        else:
            modified = True
            first_up_to_date = True
            if not compile_target(target, makefilepath, release=release):
                return False

    if modified:
        save_dependencies_to_cache(targets, makefilepath)

    return True


def compile_all(targets, makefilepath, release):
    for target in targets:
        if not compile_target(target, makefilepath, release=release):
            return False

    save_dependencies_to_cache(targets, makefilepath)
    return True


def compile_target(target, makefilepath, release):
    try:
        logv('\nCompiling: {}'.format(target['output']))
        compiler_fn = target['compiler_fn']
        compiler_fn(target['input'], target['output'], release=release, **target['kwargs'])
        load_dependencies_for_target(target, makefilepath)
        return True
    except StaticCompilerError as e:
        log(str(e))
        return False

