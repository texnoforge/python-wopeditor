from configparser import InterpolationSyntaxError
import sys, os
from pathlib import Path

from kivy.app import App
from kivy.config import Config
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import NumericProperty, StringProperty
from kivy.properties import BooleanProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

from wopeditor.texnomagic.abcs import TexnoMagicAlphabets
from wopeditor.texnomagic.drawing import TexnoMagicDrawing
from wopeditor.texnomagic import common

from wopeditor.screens.abcs import AbcsScreen
from wopeditor.screens.abc import AbcScreen
from wopeditor.screens.symbol import SymbolScreen
from wopeditor.screens.drawing import DrawingScreen
from wopeditor.screens.newdrawing import NewDrawingScreen

from wopeditor.widgets.errorpopup import ErrorPopup


if getattr(sys, 'frozen', False):
    # PyInstaller
    APP_PATH = sys._MEIPASS
else:
    APP_PATH = os.path.dirname(os.path.abspath(__file__))


Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


SCREENS = {
    'abcs': AbcsScreen,
    'abc': AbcScreen,
    'symbol': SymbolScreen,
    'drawing': DrawingScreen,
    'newdrawing': NewDrawingScreen,
}


class WoPEditorApp(App):
    index = NumericProperty(-1)
    current_title = StringProperty()
    screen_names = ListProperty([])

    def build(self):
        self.title = 'Words of Power Editor'
        self.screens = {}
        self.screens_available = ['abcs']
        self.base_path = Path(APP_PATH)
        return ScreenManager()

    def on_start(self):
        Logger.info("WoPeditor: base path: %s" % self.base_path)
        self.load_abcs()
        self.goto_abcs()
        # DEBUG
        #self.goto_abc(self.abcs.abcs['user'][0])
        #self.goto_symbol(self.abc.symbols[1])
        #self.goto_drawing(self.symbol.drawings[0])

    @property
    def core_abcs_path(self):
        return self.base_path / 'data' / 'alphabets'

    @property
    def user_abcs_path(self):
        return common.get_appdata_path() / 'alphabets'

    def get_screen(self, screen_name):
        screen = self.screens.get(screen_name)
        if not screen:
            screen = self.load_screen(screen_name)
        return screen

    def goto_screen(self, screen, back=False):
        if back:
            direction = 'right'
        else:
            direction = 'left'

        return self.root.switch_to(screen, direction=direction)

    def load_screen(self, screen_name):
        screen_class = SCREENS[screen_name]
        screen = screen_class()
        assert screen
        self.screens[screen_name] = screen
        return screen

    def load_abcs(self):
        paths = {
            'core': self.core_abcs_path,
            'user': self.user_abcs_path,
            'community': Path("c:/invalid/path"),
        }
        self.abcs = TexnoMagicAlphabets(paths)
        self.abcs.load()

    def goto_abcs(self, back_from=None):
        screen = self.get_screen('abcs')
        if not back_from:
            screen.update_abcs(self.abcs)
        self.goto_screen(screen, back=back_from)

    def goto_abc(self, abc=None, back_from=None):
        screen = self.get_screen('abc')
        if abc:
            self.abc = abc
            screen.update_abc(abc)
        self.goto_screen(screen, back=back_from)

    def goto_symbol(self, symbol=None, back_from=None):
        screen = self.get_screen('symbol')
        if symbol:
            self.symbol = symbol
            screen.update_symbol(symbol)
        self.goto_screen(screen, back=back_from)

    def goto_drawing(self, drawing):
        screen = self.get_screen('drawing')
        self.drawing = drawing
        screen.update_drawing(drawing)
        self.goto_screen(screen)

    def goto_new_drawing(self):
        screen = self.get_screen('newdrawing')
        screen.update()
        self.goto_screen(screen)

    def new_symbol(self):
        popup = Factory.NewSymbolPopup()

    def new_abc(self):
        popup = Factory.NewAbcPopup()

    def add_new_symbol(self, symbol):
        self.abc.save_new_symbol(symbol)
        Logger.info("symbol: saved new symbol: %s", symbol)
        self.get_screen('abc').update_abc()

    def add_new_abc(self, abc):
        self.abcs.save_new_alphabet(abc)
        Logger.info("abc: saved new alphabet: %s", abc)
        self.get_screen('abcs').update_abcs()

    def save_drawing(self):
        screen = self.get_screen('newdrawing')
        curves = screen.ids['drawing_area'].curves
        if not curves:
            ErrorPopup(
                title="ERROR: empty drawing",
                text="draw something to save first").open()
            return
        drawing = TexnoMagicDrawing(curves=curves)
        drawing.normalize()
        self.symbol.save_new_drawing(drawing)
        self.goto_symbol(self.symbol, back_from='newdrawing')


if __name__ == "__main__":
    WoPEditorApp().run()