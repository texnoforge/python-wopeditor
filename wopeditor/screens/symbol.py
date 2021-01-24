from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class SymbolScreen(Screen):
    symbol = None
    drawings = []

    def update_symbol(self, symbol=None):
        if symbol:
            if symbol == self.symbol:
                return
            self.symbol = symbol
        drawings_list = self.ids['drawings_list']
        drawings_list.clear_widgets()
        for drawing in self.symbol.drawings:
            b = DrawingButton(drawing=drawing)
            drawings_list.add_widget(b)
        self.ids['header'].title = self.symbol.name


class DrawingButton(Button):
    def __init__(self, **kwargs):
        self.drawing = kwargs.pop('drawing', None)
        if self.drawing:
            kwargs['text'] = self.drawing.name
        super().__init__(**kwargs)