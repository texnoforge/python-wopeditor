from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.graphics import Color, Ellipse, Line, PushMatrix, PopMatrix, Rotate
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image

from wopeditor import platform
from wopeditor.texnomagic import common
from wopeditor.widgets.nicescrollview import NiceScrollView

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
                    on_release: app.goto_new_drawing()
                SideButton:
                    text: "open dir"
                    on_release: root.open_dir()
                SideButton:
                    text: "train model"
                    on_release: app.train_symbol_model()
                ModelPreview:
                    id: model_preview
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


<ModelPreview>:
    size_hint_y: None
    height: self.width
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
        self.ids['model_preview'].update_model(model=self.symbol.model)

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


class ModelPreview(Widget):
    model = None

    def __init__(self, **kwargs):
        model = kwargs.pop('model', None)
        super().__init__(**kwargs)
        if model:
            self.update_model(model=model)
        self.bind(size=self.update_model,
                  pos=self.update_model)

    def update_model(self, *arg, model=None):
        if model is not None:
            self.model = model

        self.canvas.clear()
        if not self.model or not hasattr(self.model.gmm, 'means_'):
            return

        with self.canvas:
            Color(0.7, 0.0, 0.0)

            means = self.model.gmm.means_
            for i, cov in enumerate(self.model.gmm.covariances_):
                v, w = np.linalg.eigh(cov)
                u = w[0] / np.linalg.norm(w[0])
                angle = np.arctan2(u[1], u[0])
                angle = 180 * angle / np.pi  # convert to degrees
                v = 2. * np.sqrt(2.) * np.sqrt(v)
                # ell = mpl.patches.Ellipse(means[i, :2], v[0], v[1],
                #                     180 + angle, color=color)
                asize = np.array(self.size)
                center = means[i, :2] / 1000 * asize + self.pos
                size = v / 1000 * asize
                pos = center - (size / 2)
                PushMatrix()
                Rotate(origin=center, angle=angle)
                Ellipse(
                    pos=pos,
                    size=size,
                )
                PopMatrix()
