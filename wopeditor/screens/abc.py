from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from wopeditor.texnomagic.symbol import TexnoMagicSymbol
from wopeditor.texnomagic import common 
from wopeditor.widgets.labeledtextinput import LabeledTextInput
from wopeditor.widgets.focusbutton import FocusButton
from wopeditor.widgets.sidebar import Sidebar, SideButton


class AbcScreen(Screen):
    abc = None
    symbols = []

    def update_abc(self, abc=None):
        if abc:
            self.abc = abc
        if not self.abc:
            return
        symbols_list = self.ids['symbols_list']
        symbols_list.clear_widgets()
        for symbol in self.abc.symbols:
            b = SymbolButton(symbol=symbol)
            symbols_list.add_widget(b)
        self.ids['header'].title = self.abc.name

    def show_create_new_symbol(self):
        NewSymbolPopup().open()

    def open_dir(self):
        common.open_dir(self.abc.info_path, select=True)


class SymbolButton(Button):
    def __init__(self, **kwargs):
        self.symbol = kwargs.pop('symbol', None)
        if self.symbol:
            kwargs['text'] = self.symbol.name
        super().__init__(**kwargs)


class NewSymbolPopup(Popup):
    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        super().__init__(**kwargs)
        self.symbol = None

    def on_confirm(self):
        pass

    def confirm(self):
        missing = []
        name = self.ids['name_input'].text
        meaning = self.ids['meaning_input'].text
        if not name:
            missing.append('name')
        if not meaning:
            missing.append('meaning')
        if missing:
            msg = "missing required input: %s" % ", ".join(missing)
            self.ids['warning_label'].text = msg
        else:
            self.symbol = TexnoMagicSymbol(name=name, meaning=meaning)
            self.dispatch('on_confirm')
            self.dismiss()