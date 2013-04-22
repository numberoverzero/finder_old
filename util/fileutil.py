import os
import strutil


_root = None


def set_root(file):
    '''
    Pass in __file__ from a script to set that script's directory as the root for
    determining absolute paths to resources
    '''
    global _root
    _root = os.path.dirname(os.path.realpath(file))


def abs_path(filename):
    '''Absolute path from _root '''
    if not _root:
        raise ValueError("Unknown root.  Use set_root(__file__) from a script in the root directory first.")
    return os.path.join(_root, filename)


def load_file(filename):
    '''Returns the contents of the given file in the data folder.'''
    path = abs_path(filename)
    with open(path) as f:
        data = f.read()
        return strutil.sanitize(data)


def load_config(config, filename):
    '''key = value in filename becomes config[key] = value'''
    config_lines = load_file(filename).split(u'\n')
    for line in config_lines:
        line = strutil.until(line, u'#')
        if not line or u'=' not in line:
            continue
        key, value = line.split(u'=', 1)
        key, value = key.strip(), value.strip()
        config[key] = value
