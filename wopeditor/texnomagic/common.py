import re
import os
from pathlib import Path
import subprocess


def name2fn(name):
    fn = re.sub(r'\s+', '-', name.lower())
    return fn


def open_dir(path, select=False):
    cmd = r'explorer '
    if select:
        cmd += r'/select,'
    cmd += '"%s"' % path
    subprocess.Popen(cmd)


def get_data_path():
    appdata = os.environ.get('APPDATA')
    if appdata:
        # windows system
        p = Path(appdata) / 'Words of Power'
    else:
        # normal system :)
        p = Path.home() / '.words_of_power'
    return p


DATA_PATH = get_data_path()
USER_DATA_PATH = DATA_PATH / 'user'
MODS_DATA_PATH = DATA_PATH / 'mods'
EXPORT_DATA_PATH = DATA_PATH / 'export'


ALPHABETS_DIR = 'alphabets'
