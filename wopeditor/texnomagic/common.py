import re
import subprocess


def name2fn(name):
    fn = re.sub('\s+', '-', name.lower())
    return fn


def open_dir(path):
    cmd = r'explorer /select,"%s"' % path
    subprocess.Popen(cmd)