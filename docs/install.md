# Installation

## Native Packages

### Windows

On Windows you can use installer which is provided with each [release][releases].

Choose a [release][releases], select **Assets**, download `wopeditor-*_installer.exe` file and run it.

#### Recommended Windows Download

* [wopeditor-0.0.1_installer.exe](https://github.com/texnoforge/wopeditor/releases/download/v0.0.1/wopeditor-0.0.1_installer.exe)
  ([v0.0.1 release][v0.0.1])

### Other Systems

Packages aren't available for other platforms, please use the Source.


## Running from Source (easy, no compilation)

You should be ablo to run `wopeditor` on many different systems supported by
Kivy framework including Linux, Windows, Mac, and Android.

### Requirements

First, you need to install following requirements:

* [Python 3](https://www.python.org/downloads/) - developed and tested with
  **Python 3.9** (lower versions might or might not work)

* [Kivy](https://kivy.org/doc/stable/gettingstarted/installation.html)
  UI framework - you **need version 2.0.0 or newer**

**tl;dr** install Python 3 which includes `pip` and then:

```
pip install kivy
```

### Getting Sources

You can get latest sources using `git`:

```
git clone https://github.com/texnoforge/wopeditor
cd wopeditor
```

Or you can download [release](https://github.com/texnoforge/wopeditor/releases)
archive and unpack it somewhere.


### Starting wopeditor

After you've installed requirements above and obtained `wopeditor` sources, enter its top directory and run following command depending on your system:


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
