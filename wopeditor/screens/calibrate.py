from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout

from kivy.logger import Logger


Builder.load_string('''
<CalibrateScreen>:
    name: "calibrate"

    GridLayout:
        cols: 1
        padding: [10, 10]

        Header:
            id: header
            title: "calibrate alphabet symbol models"
            on_press_back: app.goto_abc(back_from=root.name)

        BoxLayout:
            Sidebar:
                id: sidebar
                SideButton:
                    text: "calibrate"
                    on_press: root.calibrate()
                FloatLayout:
                    #Filler

            NiceScrollView:
                id: main_scroll
                StackLayout:
                    id: symbols_list
                    size_hint: 1, None
                    height: max(main_scroll.height, self.minimum_height)
                    spacing: 10
''')


class CalibrateScreen(Screen):
    abc = None

    def update(self, abc=None):
        if abc:
            self.abc = abc
        name = 'alphabet'
        if self.abc:
            name = self.abc

        self.ids['header'].title = "calibrate %s symbol models" % abc.name
        self.ids['symbols_list'].clear_widgets()

    def calibrate(self):
        Logger.info("abc: calibrating %s", self.abc)
