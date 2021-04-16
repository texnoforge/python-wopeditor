import subprocess

from kivy.logger import Logger


def open_dir(path, select=False):
    Logger.info("platform: trying to open in file manager: %s", path)
    cmd = r'explorer '
    if select:
        cmd += r'/select,'
    cmd += '"%s"' % path
    try:
        subprocess.Popen(cmd)
    except Exception:
        Logger.warning("platform: unable to open: %s", path)
