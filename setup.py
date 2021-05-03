import setuptools


# get version
exec(open('wopeditor/__init__.py').read())


setuptools.setup(
    version=__version__)
