from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class DrawingScreen(Screen):
    symbol = None
    drawings = []

    def update_symbol(self, symbol=None):
        if symbol:
            if symbol == self.symbol:
                return
            self.symbol = symbol
        drawing_preview = self.ids['drawing_preview']
        drawing_preview.text = self.symbol.name
        self.ids['header'].title = self.symbol.name