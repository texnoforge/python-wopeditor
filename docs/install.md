# Installation

## Native Packages

### Windows

On Windows you can use installer which is provided with each
[release][releases].

Choose a [release][releases], select **Assets**, download `wopeditor-*_installer.exe` file and run it.

#### Recommended Windows Download

* [wopeditor-0.0.1_installer.exe](https://github.com/texnoforge/wopeditor/releases/download/v0.0.1/wopeditor-0.0.1_installer.exe)
  ([v0.0.1 release][v0.0.1])

### Other Systems

Packages aren't available for other platforms, please use the Source.


## Running from Source (easy, no compilation)

You should be ablo to run `wopeditor` from source on many different systems
supported by Kivy framework including Linux, Windows, Mac, and Android.


### Requirements

#### Python 3

`wopeditor` is written **Python 3.9**, lower versions might or might not work (3.7+ is worth a try).

On windows get [Python 3 installer](https://www.python.org/downloads/) which
includes `pip`.

On linux distros, it's usually available as `python3` package.

Debian and clones using `.deb` (Ubuntu, Mint, ...):

```
sudo apt install python3 python3-pip
```

Fedora, CentOS, SUSE and other `.rpm` distros:

```
sudo dnf install python3 python3-pip
```

#### Required Python Modules

Required modules are listed in `requirements.txt` file and are all
available from PyPI to be installed using `pip`:

```
pip install -r requirements.txt
```

On some systems you need to use `pip3` instead to invoke Python 3 `pip` (as
opposed to Python 2 which won't work):

```
pip3 install -r requirements.txt
```

A short summary of used modules:

* [Kivy](https://kivy.org/doc/stable/gettingstarted/installation.html)
  python UI framework - you **need version 2.0.0 or newer**

* [Trio](https://trio.readthedocs.io/en/stable/) python async module

Please refer to `requirements.txt` file for up-to-date list of requirements,


### Getting Sources

You can get latest sources using `git`:

```
git clone https://github.com/texnoforge/wopeditor
cd wopeditor
```

Or you can download [release](https://github.com/texnoforge/wopeditor/releases)
archive and unpack it somewhere.


### Starting wopeditor

After you've installed requirements above and obtained `wopeditor` sources,
enter top directory and run following command depending on your system:


#### any system

```
python wopeditor.py
```

#### linux/unix

```
./wopeditor.py
```

#### windows

```
wopeditor.bat
```


[releases]: https://github.com/texnoforge/wopeditor/releases
[v0.0.1]: https://github.com/texnoforge/wopeditor/releases/tag/v0.0.1


### Tested Operating Systems

`wopeditor` has been tested to work on following systems:

* Windows 10
* Arch Linux

If you managed to run `wopeditor` on other OS, please add it to this list.

You can edit this doc at `docs/install.md` and submit a MR or just open [New Issue] with your success and I'll add it to the list - thank you ❤

[New Issue]: https://github.com/texnoforge/wopeditor/issues
