# Words of Power Editor

**Words of Power Editor** is a free open source app for creation,
modification, distribution, and machine recognition of custom magic
symbols in TexnoMagic format used in upcoming
[texnoforge](https://texnoforge.dev)
game
[Words of Power](https://texnoforge.dev/pages/words-of-power.html)
and any other games/apps that choose to adopt this free format and/or tool.

The goal is to provide users with means to create and share their own custom
symbols by drawing them with mouse or any other pointing device. After
collecting enough drawings of a symbol, a model can be trained and used to
recognize the symbol from user input.

Entire alphabets of symbols with names, meanings, and different drawings
can be created including models to recognize individual symbols drawn by
users in real-time.


## Status

### development just started, come back later

There is only a bare skeleton of UI in Kivy at the moment ¯\\\_(ツ)\_/¯


## TexnoMagic

I created TexnoMagic format after prototyping serveral systems for magic
symbol recognition and invocation as well as systems for creating magic
language based on symbols. You can read my posts about
[Theory of Magic](https://texnoforge.dev/words-of-power-devlog-1-theory-of-magic.html) and
[Invocation of Magic](https://texnoforge.dev/words-of-power-devlog-2-invocation-of-magic.html)
to get better idea of what I'm trying to achieve.


## Usage

Get `python` 3 and `kivy >= 2.0.0` and then run

```
python wopeditor/wopeditor.py
```

You can also use `wopeditor.sh` (linux) or `wopeditor.bat` (windows) script
in the project root.
