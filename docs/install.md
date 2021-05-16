# Installation

## Install using pip (recommended)

`python-wopeditor` is available from [PyPI](https://pypi.org/project/wopeditor/) ᕕ( ᐛ )ᕗ

Make sure you have Python 3 and `pip` installed and then simply run

```
pip install wopeditor
```

To upgrade to latest version:

```
pip install --upgrade wopeditor
```

Once installed, run using
```
python -m wopeditor
```

## Windows Installer

On Windows you can alternatively use installer which is provided with each
[release][releases].

Choose a [release][releases], select **Assets**, download `wopeditor-*_installer.exe` file and run it.

You might get false positives from security software because `wopeditor` doesn't have any kind of commercial certification.

Install using `pip` (as described above) instead if you don't want to run the `.exe`.

### Recommended Windows Download

* [wopeditor-0.1.1_installer.exe](https://github.com/texnoforge/python-wopeditor/releases/download/v0.1.1/wopeditor-0.1.1_installer.exe)
  ([v0.1.1 release][v0.1.1])


# Running from Source

You should be ablo to run `wopeditor` from source on many different systems
supported by Kivy framework including Linux and Windows.

## Getting Sources

You can get latest sources using `git`:

```
git clone https://github.com/texnoforge/wopeditor
cd wopeditor
```

Or you can download [release](https://github.com/texnoforge/wopeditor/releases)
archive and unpack it somewhere.


## Requirements

### Python 3

`wopeditor` is written **Python 3.9**, lower versions might or might not work (3.7+ is worth a try).

On windows get [Python 3 installer](https://www.python.org/downloads/) which
includes `pip`.

On linux distros, it's usually available as `python3` package. Make sure to install `pip` as well.

Debian and clones using `.deb` (Ubuntu, Mint, ...):

```
sudo apt install python3 python3-pip
```

Fedora, CentOS, SUSE and other `.rpm` distros:

```
sudo dnf install python3 python3-pip
```

### Required Python Modules

Required modules are listed in `requirements.txt` file and are all
available from PyPI to be installed using `pip`.

They should be automatically installed during `wopeditor` installation, no need
to install them manually.

A short summary of used python modules:

* [Kivy](https://kivy.org/doc/stable/gettingstarted/installation.html):
  UI framework - you **need version 2.0.0 or newer**

* [Trio](https://trio.readthedocs.io/en/stable/): python async module


## Install wopeditor Module

Run following in top level of `wopeditor` source dir:

```
pip install .
```

If you want to modify `wopeditor`, use `--editable` mode:

```
pip install -e .
```

or directly:

```
python setup.py develop
```


## Starting wopeditor

After you've installed `wopeditor` module, you can run it from anywhere:

```
python -m wopeditor
```

Furthermore, a `wopeditor` script is installed somewhere by `pip`. If it
happens to be in your `$PATH`, you can use it instead:

```
wopeditor
```


[releases]: https://github.com/texnoforge/python-wopeditor/releases
[v0.1.1]: https://github.com/texnoforge/pythonwopeditor/releases/tag/v0.1.1


# Tested Operating Systems

`python-wopeditor` has been tested to work on following systems:

* Windows 10
* Arch Linux
