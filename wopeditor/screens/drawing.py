from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from wopeditor import platform
from texnomagic import common
from wopeditor.widgets.drawingpreview import DrawingPreview


Builder.load_string('''
<DrawingScreen>:
    name: "drawing"

    GridLayout:
        cols: 1
        padding: [10, 0]

        Header:
            id: header
            on_press_back: app.goto_symbol(back_from=root.name)

        BoxLayout:
            Sidebar:
                id: sidebar
                SideButton:
                    text: "open dir"
                    on_press: root.open_dir()
                SideButton:
                    text: "delete drawing"
                    on_press: app.delete_drawing()
                FloatLayout:
                    #Filler

            DrawingPreview:
                id: drawing_preview
''')


class DrawingScreen(Screen):
    drawing = None

    def update_drawing(self, drawing=None):
        if drawing:
            self.drawing = drawing
        if not self.drawing:
            return

        drawing_preview = self.ids['drawing_preview']
        drawing_preview.update_drawing(drawing=self.drawing)
        self.ids['header'].title = self.drawing.name

    def open_dir(self):
        platform.open_dir(self.drawing.path, select=True)
