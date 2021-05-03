from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from wopeditor import platform
from texnomagic import common
from wopeditor.widgets.drawingpreview import DrawingPreview


Builder.load_string('''
<ModelScreen>:
    name: "model"

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
                    text: "train model"
                    on_press: root.train_model()
                BoxLayout:
                    size_hint_y: None
                    height: dp(30)
                    Label:
                        text: "# gauss: "
                        size_hint_x: None
                        width: self.texture_size[0]
                    TextInput:
                        id: n_gauss
                        text: "5"
                        size_hint_x: None
                        width: dp(50)
                        multiline: False
                        write_tab: False
                FloatLayout:
                    #Filler

            ModelPreview:
                id: model_preview
''')


class ModelScreen(Screen):
    symbol = None

    def update_model(self, symbol=None):
        if symbol:
            self.symbol = symbol
        if not self.symbol:
            return

        model_preview = self.ids['model_preview']
        model_preview.update_symbol(symbol=self.symbol)
        self.ids['header'].title = "%s model" % self.symbol.name
        self.ids['n_gauss'].text = str(self.symbol.model.n_gauss)

    def open_dir(self):
        platform.open_dir(self.symbol.model.path, select=True)

    def train_model(self):
        n_gauss = int(self.ids['n_gauss'].text)
        self.symbol.model.n_gauss = n_gauss
        App.get_running_app().train_model()
