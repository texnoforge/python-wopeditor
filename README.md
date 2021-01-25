# Words of Power Editor

**Words of Power Editor** is a free open source app for creation,
modification, distribution, and machine recognition of custom magic
symbols in **TexnoMagic** format used in upcoming
[texnoforge](https://texnoforge.dev)
game
[Words of Power](https://texnoforge.dev/pages/words-of-power.html)
and any other games/apps that choose to adopt this free format and/or tool.

The goal is to provide users with means to create and share their own custom
symbols by drawing them with mouse or any other pointing device. After
collecting enough drawings of a symbol, a model can be trained and used to
recognize the symbol from user input.

Entire alphabets of symbols with names, meanings, and graphical
representations be created including models to recognize individual symbols
drawn by users in real-time.


## Status

### development just started, come back later

There is only a bare skeleton of UI in Kivy at the moment ¯\\\_(ツ)\_/¯


## TexnoMagic

I created **TexnoMagic** format after prototyping serveral systems for magic
symbol recognition and invocation as well as systems for creating magic
language based on symbols. You can read my posts about
[Theory of Magic](https://texnoforge.dev/words-of-power-devlog-1-theory-of-magic.html) and
[Invocation of Magic](https://texnoforge.dev/words-of-power-devlog-2-invocation-of-magic.html)
to get better idea of what I'm trying to achieve.

`wopeditor.texnomagic` module is dedicated to technical side of things and I
plan to make it a dedicated module available from PyPI once it matures but
for now it's more convenient to have everything in one repository.

`texnomagic` is going to use [SciPy](https://www.scipy.org/) python
scientific package to train symbol models using GMMs and recognize symbols
using these models. I've already prototyped this and confirmed it works, this
is an attempt at serious implementation which can be reused in other software
and/or used as a reference.


## Requirements

You should be ablo to run `wopeditor` on many different systems supported by
Kivy framework including Linux, Windows, Mac, and Android.

You need to install following requirements:

* [Python 3](https://www.python.org/downloads/) - developed and tested with
  **Python 3.9** (lower versions might or might not work)

* [Kivy](https://kivy.org/doc/stable/gettingstarted/installation.html)
  UI framework - you **need version 2.0.0 or newer**


## Usage

After you installed requirements above, run


### on any system

```
python wopeditor.py
```

### on linux/unix

```
./wopeditor.py
```

### on windows

```
wopeditor.bat
```


## Current Features

* code is split into small files arranged in a sustainable modular structure including UI
* clean reusable UI code for loading and displaying alphabets/symbols/drawings from disk
* separate `wopeditor.texnomagic` module to easily interface and work with
  symbol/alphabet data on disk - logic separate from UI
* `wopeditor` module can be imported locally but it's also ready be packaged using
  `setuptools` for PyPI, using `PyInstaller` for Windows, and using native
  packaging tools for linux distros


## Planned Features

* create new alphabets and symbols
* draw symbols using mouse and save to files
* train models from saved symbol drawings
* recognize symbols from drawings using models
* much more