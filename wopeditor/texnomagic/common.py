import re
import os
from pathlib import Path
import subprocess


def name2fn(name):
    fn = re.sub('\s+', '-', name.lower())
    return fn


def open_dir(path, select=False):
    cmd = r'explorer '
    if select:
        cmd += r'/select,'
    cmd += '"%s"' % path
    subprocess.Popen(cmd)


def get_appdata_path():
    appdata = os.environ.get('APPDATA')
    if appdata:
        # windows system
        p = Path(appdata) / 'Words of Power'
    else:
        # normal system :)
        p = Path.home() / '.words_of_power'
    return p
