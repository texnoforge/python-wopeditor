from kivy.app import App
from kivy.core.text import Label as CoreLabel
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image

from wopeditor import platform
from texnomagic import common
from wopeditor.widgets.nicescrollview import NiceScrollView
from wopeditor.widgets.modelpreview import ModelPreview

import numpy as np


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
                    on_press: app.goto_new_drawing()
                SideButton:
                    text: "symbol model"
                    on_press: app.goto_model()
                ModelPreview:
                    id: model_preview
                    height: self.width
                    size_hint_y: None
                    on_press: app.goto_model()
                SideButton:
                    text: "open dir"
                    on_press: root.open_dir()
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
    size_hint: None, None
    size: [dp(200), dp(220)]
    text_size: self.size
    valign: 'bottom'
    halign: 'center'
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
        self.update_model()

    def update_model(self):
        self.ids['model_preview'].update_symbol(symbol=self.symbol)

    def open_dir(self):
        platform.open_dir(self.symbol.info_path, select=True)


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
        padding_r = 0.1
        lw = 2
        size = list(map(lambda x: x * (1 - 2 * padding_r), self.size))
        pos = [self.pos[0] + size[0] * padding_r, self.pos[1] + size[1] * padding_r]

        if not self.text:
            self.text = self.drawing.name
        self.canvas.clear()

        with self.canvas:
            # label
            label = CoreLabel(text=self.text, font_size=20)
            label.refresh()
            ltex = label.texture
            lpos = [self.x + (self.width - ltex.size[0]) / 2, self.y + 5]

            # drawing
            dpos = [pos[0], pos[1] +  ltex.height]
            dsize = [size[0], size[1] - ltex.height]
            if self.drawing:
                Color(1, 1, 1)
                for curve in self.drawing.curves_fit_area(dpos, dsize):
                    Line(points=curve.tolist(), width=lw)
            else:
                Color(0.06, 0.06, 0.06)
                Rectangle(pos=dpos, size=dsize)

            Color(1, 1, 1)
            self.canvas.add(Rectangle(size=ltex.size, pos=lpos, texture=ltex))


    def on_press(self):
        App.get_running_app().goto_drawing(self.drawing)
