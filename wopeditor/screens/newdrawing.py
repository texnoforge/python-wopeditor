from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout

from wopeditor.widgets.drawingpreview import DrawingPreview


Builder.load_string('''
<NewDrawingScreen>:
    name: "newdrawing"

    GridLayout:
        cols: 1
        padding: [10, 10]

        Header:
            id: header
            title: "new symbol drawing"
            on_press_back: app.goto_symbol(back_from=root.name)

        BoxLayout:
            Sidebar:
                id: sidebar
                SideButton:
                    text: "clear"
                    on_press: root.ids['drawing_area'].clear()
                SideButton:
                    text: "save"
                    on_press: app.save_drawing()
                FloatLayout:
                    #Filler

            DrawingArea:
                id: drawing_area

<DrawingArea>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            width: 1
            rectangle: self.x, self.y, self.width, self.height
            dash_length: 6
            dash_offset: 4
''')


class NewDrawingScreen(Screen):
    def update(self):
        self.ids['drawing_area'].clear()


class DrawingArea(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_drawing = False
        self.points = []
        self.curves = []
        self.line = None

    def start_draw(self, first_point):
        self.points = [first_point]
        self.is_drawing = True
        self.curves.append(self.points)
        with self.canvas.after:
            Color(1.0, 1.0, 1.0)
            self.line = Line(points=self.points)

    def end_draw(self):
        self.is_drawing = False

    def clear(self):
        self.end_draw()
        self.points = []
        self.curves = []
        self.canvas.after.clear()

    def on_touch_down(self, touch):
        if touch.x < self.x or touch.y > self.y + self.height:
            return
        self.start_draw(touch.pos)

    def on_touch_up(self, touch):
        self.end_draw()

    def on_touch_move(self, touch):
        if self.is_drawing:
            self.points.append(touch.pos)
            self.line.points = self.points
