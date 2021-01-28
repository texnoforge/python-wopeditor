from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.clock import Clock


Builder.load_string('''
<DrawingPreview>:
    size_hint: 1, 1
''')




class DrawingPreview(Widget):
    drawing = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_drawing)

    def update_drawing(self, *args, drawing=None):
        if drawing:
            self.drawing = drawing
        if not self.drawing:
            return
        self.canvas.clear()
        with self.canvas:
            Color(0.7, 0.7, 0.0)
            for curve in self.drawing.curves_fit_area(self.pos, self.size):
                Line(points=curve)