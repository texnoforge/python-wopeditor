from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from wopeditor.texnomagic import common
from wopeditor.widgets.nicescrollview import NiceScrollView


Builder.load_string('''
<SymbolScreen>:
    name: "symbol"

    GridLayout:
        cols: 1
        padding: [10, 0]

        Header:
            id: header
            on_press_back: app.goto_abc(back_from=root.name)

        BoxLayout:
            Sidebar:
                id: sidebar
                SideButton:
                    text: "new drawing"
                    on_release: app.goto_new_drawing()
                SideButton:
                    text: "open dir"
                    on_release: root.open_dir()
                FloatLayout:
                    #Filler

            NiceScrollView:
                id: main_scroll
                StackLayout:
                    id: drawings_list
                    size_hint: 1, None
                    height: max(main_scroll.height, self.minimum_height)
                    spacing: 10


<DrawingButton>:
    size: [160, 160]
    size_hint: None, None
''')


class SymbolScreen(Screen):
    symbol = None
    drawings = []

    def update_symbol(self, symbol=None):
        if symbol:
            self.symbol = symbol
        if not self.symbol:
            return
        drawings_list = self.ids['drawings_list']
        drawings_list.clear_widgets()
        for drawing in self.symbol.drawings:
            b = DrawingButton(drawing=drawing)
            drawings_list.add_widget(b)
        title = "%s (%s)" % (self.symbol.name, self.symbol.meaning)
        self.ids['header'].title = title

    def open_dir(self):
        common.open_dir(self.symbol.info_path, select=True)


class DrawingButton(Button):
    drawing = None

    def __init__(self, **kwargs):
        drawing = kwargs.pop('drawing', None)
        super().__init__(**kwargs)
        if drawing:
            self.update_drawing(drawing=drawing)
        self.bind(size=self.update_drawing,
                  pos=self.update_drawing)

    def update_drawing(self, *_, drawing=None):
        if drawing:
            self.drawing = drawing
        if not self.drawing:
            return

        padding_r = 0.1
        size = list(map(lambda x: x * (1 - 2 * padding_r), self.size))
        pos = [self.pos[0] + size[0] * padding_r, self.pos[1] + size[1] * padding_r]

        if not self.text:
            self.text = self.drawing.name
        self.canvas.after.clear()
        #self.canvas.clear()
        with self.canvas.after:
            Color(0.7, 0.7, 0.0)
            for curve in self.drawing.curves_fit_area(pos, size):
                Line(points=curve.tolist())

    def on_release(self):
        App.get_running_app().goto_drawing(self.drawing)