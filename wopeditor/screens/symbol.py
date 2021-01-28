from kivy.graphics import Color, Line
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
    drawing = None

    def __init__(self, **kwargs):
        drawing = kwargs.pop('drawing', None)
        super().__init__(**kwargs)
        if drawing:
            self.update_drawing(drawing=drawing)
        self.bind(size=self.update_drawing,
                  pos=self.update_drawing)

    def update_drawing(self, *args, drawing=None):
        if drawing:
            self.drawing = drawing
        if not self.drawing:
            return

        padding_r = 0.1
        size = list(map(lambda x: x * (1 - 2 * padding_r), self.size))
        pos = [self.pos[0] + size[0] * padding_r, self.pos[1] + size[1] * padding_r]

        self.text = self.drawing.name
        self.canvas.after.clear()
        #self.canvas.clear()
        with self.canvas.after:
            Color(0.7, 0.7, 0.0)
            for curve in self.drawing.curves_fit_area(pos, size):
                Line(points=curve)