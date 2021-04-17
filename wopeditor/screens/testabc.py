from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout

from wopeditor.widgets.drawingarea import DrawingArea


Builder.load_string('''
<TestAbcScreen>:
    name: "testabc"

    GridLayout:
        cols: 1
        padding: [10, 10]

        Header:
            id: header
            title: "test alphabet recognition"
            on_press_back: app.goto_abc(back_from=root.name)

        BoxLayout:
            Sidebar:
                id: sidebar
                SideButton:
                    text: "clear"
                    on_press: root.ids['drawing_area'].clear()
                FloatLayout:
                    #Filler

            DrawingArea:
                id: drawing_area
                on_touch_up: app.recognize_symbol(self.curves)
''')


class TestAbcScreen(Screen):
    abc = None

    def update(self, abc=None):
        if abc:
            self.abc = abc
        name = 'alphabet'
        if self.abc:
            name = abc.name
        self.ids['header'].title = "test %s recognition" % name
        self.ids['drawing_area'].clear()
