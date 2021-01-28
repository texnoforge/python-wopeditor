from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from wopeditor.widgets.drawingpreview import DrawingPreview


class DrawingScreen(Screen):
    drawing = None

    def update_drawing(self, drawing=None):
        if drawing:
            if drawing == self.drawing:
                return
            self.drawing = drawing
        drawing_preview = self.ids['drawing_preview']
        drawing_preview.update_drawing(drawing=self.drawing)
        self.ids['header'].title = self.drawing.name