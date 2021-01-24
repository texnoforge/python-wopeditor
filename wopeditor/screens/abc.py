from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class AbcScreen(Screen):
    abc = None
    symbols = []

    def update_abc(self, abc=None):
        if abc:
            if abc == self.abc:
                return
            self.abc = abc
        symbols_list = self.ids['symbols_list']
        symbols_list.clear_widgets()
        for symbol in self.abc.symbols.values():
            b = SymbolButton(symbol=symbol)
            symbols_list.add_widget(b)
        self.ids['header'].title = self.abc.name


class SymbolButton(Button):
    def __init__(self, **kwargs):
        self.symbol = kwargs.pop('symbol', None)
        if self.symbol:
            kwargs['text'] = self.symbol.name
        super().__init__(**kwargs)