import os
from pathlib import Path

from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import NumericProperty, StringProperty
from kivy.properties import BooleanProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

from wopeditor.screens.abcs import AbcsScreen
from wopeditor.screens.abc import AbcScreen
from wopeditor.screens.symbol import SymbolScreen
from wopeditor.screens.drawing import DrawingScreen

from wopeditor.widgets.header import Header

from wopeditor.texnomagic.abcs import get_alphabets


class WoPEditorApp(App):
    index = NumericProperty(-1)
    current_title = StringProperty()
    screen_names = ListProperty([])

    def build(self):
        self.title = 'Words of Power Editor'
        self.screens = {}
        self.screens_available = ['abcs']
        self.base_path = Path(os.path.dirname(__file__)).resolve()
        self.load_abcs()
        self.goto_abcs()
        # DEBUG
        #self.goto_abc(self.abcs[0])
        #self.goto_symbol(self.abc.symbols[0])
        #self.goto_drawing(self.symbol.drawings[0])

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
        fn = self.base_path.joinpath('screens/%s.kv' % screen_name)
        Logger.warning("WoPEditor: loading screen: %s" % fn)
        screen = Builder.load_file(str(fn))
        assert screen
        self.screens[screen_name] = screen
        return screen

    def load_abcs(self):
        abcs_path = self.base_path.parent / 'data' / 'alphabets'
        self.abcs = get_alphabets(abcs_path)

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

    def new_symbol(self, abc):
        popup = Factory.NewSymbolPopup()

    def add_new_symbol(self, symbol):
        self.abc.save_new_symbol(symbol)
        Logger.info("symbol: saved new symbol: %s", symbol)
        self.get_screen('abc').update_abc()


if __name__ == "__main__":
    WoPEditorApp().run()