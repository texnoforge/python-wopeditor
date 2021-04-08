from configparser import InterpolationSyntaxError
from functools import partial
import sys, os
from pathlib import Path

import trio

from kivy.app import App
from kivy.app import async_runTouchApp
from kivy.config import Config
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import NumericProperty, StringProperty
from kivy.properties import BooleanProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

from wopeditor import __version__
from wopeditor import platform
from wopeditor.texnomagic.abcs import TexnoMagicAlphabets
from wopeditor.texnomagic.drawing import TexnoMagicDrawing
from wopeditor.texnomagic import common

from wopeditor import wopmods

from wopeditor.screens.abcs import AbcsScreen
from wopeditor.screens.abc import AbcScreen
from wopeditor.screens.symbol import SymbolScreen
from wopeditor.screens.model import ModelScreen
from wopeditor.screens.drawing import DrawingScreen
from wopeditor.screens.newdrawing import NewDrawingScreen

from wopeditor.widgets.errorpopup import ErrorPopup


if getattr(sys, 'frozen', False):
    # PyInstaller
    APP_PATH = sys._MEIPASS
else:
    APP_PATH = os.path.dirname(os.path.abspath(__file__))


Config.set('kivy', 'window_icon', 'wopeditor.ico')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')


SCREENS = {
    'abcs': AbcsScreen,
    'abc': AbcScreen,
    'symbol': SymbolScreen,
    'model': ModelScreen,
    'drawing': DrawingScreen,
    'newdrawing': NewDrawingScreen,
}


class WoPEditorApp(App):
    index = NumericProperty(-1)
    current_title = StringProperty()
    screen_names = ListProperty([])

    screens = {}
    nursery = None
    mods = None

    version = __version__

    async def app_start(self):
        """async entry point for trio"""

        async with trio.open_nursery() as nursery:
            self.nursery = nursery

            async def run_wrapper():
                await self.async_run(async_lib='trio')
                nursery.cancel_scope.cancel()

            nursery.start_soon(run_wrapper)

    def build(self):
        self.title = 'Words of Power Editor v%s' % self.version
        self.screens_available = ['abcs']
        self.base_path = Path(APP_PATH)
        return ScreenManager()

    def on_start(self):
        Logger.info("wopeditor: base path: %s" % self.base_path)
        self.load_abcs()
        self.goto_abcs()
        # schedule loading of online mods
        self.nursery.start_soon(self.load_community_mods)

        # DEBUG
        #self.goto_abc(self.abcs.abcs['user'][0])
        #self.goto_symbol(self.abc.symbols[1])
        #self.goto_drawing(self.symbol.drawings[0])

    async def load_community_mods(self):
        Logger.info("wopeditor: loading community mods in the background")
        self.mods = wopmods.get_online_mods()
        Logger.info("wopeditor: found %d community mods", len(self.mods))
        Clock.schedule_once(self.update_mods)

    def update_mods(self, *args):
        screen = self.get_screen('abcs')
        screen.update_abcs(mods=self.mods)

    @property
    def core_data_path(self):
        return self.base_path / 'data'

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
            'core': self.core_data_path / common.ALPHABETS_DIR,
            'user': common.USER_DATA_PATH / common.ALPHABETS_DIR,
            'mods': common.MODS_DATA_PATH / common.ALPHABETS_DIR,
        }
        self.abcs = TexnoMagicAlphabets(paths)
        self.abcs.load()

    def reload_abcs(self, *args):
        self.load_abcs()
        self.get_screen('abcs').update_abcs(self.abcs)

    def refresh(self, *args):
        self.reload_abcs()
        self.nursery.start_soon(self.load_community_mods)

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
        elif back_from in ['newdrawing', 'model']:
            screen.update_symbol()
        self.goto_screen(screen, back=back_from)

    def goto_drawing(self, drawing=None, back_from=None):
        screen = self.get_screen('drawing')
        if drawing:
            self.drawing = drawing
            screen.update_drawing(drawing)
        self.goto_screen(screen, back=back_from)

    def goto_model(self, back_from=None):
        screen = self.get_screen('model')
        screen.update_model(self.symbol)
        self.goto_screen(screen, back=back_from)

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
        # update alphabet screen
        self.get_screen('abc').update_abc(self.abc)
        self.goto_symbol(self.symbol, back_from='newdrawing')

    def download_mod(self, mod):
        Logger.info("mod: requesting mod download: %s", mod)
        self.nursery.start_soon(self.dl_mod, mod)

    async def dl_mod(self, mod):
        path = common.MODS_DATA_PATH / common.ALPHABETS_DIR
        Logger.info("mod: downloading mod into: %s", path)
        mod.download(path)
        Logger.info("mod: download complete: %s", mod)
        Clock.schedule_once(self.reload_abcs)

    def export_abc(self):
        Logger.info("mod: exporting alphabet: %s", self.abc)
        path = self.abc.export()
        Logger.info("mod: export complete: %s", path)
        platform.open_dir(path, select=True)

    def train_model(self):
        Logger.info("model: training symbol model from drawings: %s", self.symbol)
        self.symbol.train_model_from_drawings()
        self.symbol.model.save()
        self.get_screen('model').update_model()

    def delete_drawing(self):
        Logger.warning("drawing: DELETE drawing: %s", self.drawing)
        self.drawing.delete()
        self.symbol.load_drawings()
        self.get_screen('symbol').update_symbol()
        self.goto_symbol(back_from='drawing')

def run_app():
    trio.run(WoPEditorApp().app_start)


if __name__ == "__main__":
    run_app()
