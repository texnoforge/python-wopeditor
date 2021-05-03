from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from texnomagic.symbol import TexnoMagicSymbol
from texnomagic import common

from wopeditor import platform
from wopeditor.widgets.labeledtextinput import LabeledTextInput
from wopeditor.widgets.focusbutton import FocusButton
from wopeditor.widgets.sidebar import Sidebar, SideButton
from wopeditor.screens.symbol import DrawingButton


Builder.load_string('''
<AbcScreen>:
    name: "abc"

    GridLayout:
        cols: 1
        padding: [10, 0]

        Header:
            id: header
            on_press_back: app.goto_abcs(back_from=root.name)

        BoxLayout:
            Sidebar:
                id: sidebar
                SideButton:
                    text: "new symbol"
                    on_press: root.show_create_new_symbol()
                SideButton:
                    text: "calibrate"
                    on_press: app.goto_calibrate()
                SideButton:
                    text: "test"
                    on_press: app.goto_test_abc()
                SideButton:
                    text: "open dir"
                    on_press: root.open_dir()
                SideButton:
                    text: "export"
                    on_press: app.export_abc()
                FloatLayout:
                    #Filler

            NiceScrollView:
                id: main_scroll
                StackLayout:
                    id: symbols_list
                    size_hint: 1, None
                    height: max(main_scroll.height, self.minimum_height)
                    spacing: 10


<SymbolButton>:
    font_size: 24


<NewSymbolPopup>:
    size_hint: None, None
    width: 400
    height: name_input.height * 3 + confirm_button.height + self.title_size + dp(80)
    title: "create new symbol"
    on_open: name_input.ids['text_input'].focus = True
    on_confirm: app.add_new_symbol(self.symbol)
    BoxLayout:
        id: content
        orientation: 'vertical'
        padding: [0, 5, 0, 0]
        spacing: 5
        LabeledTextInput:
            id: name_input
            label_text: "name:"
            focus: True
        LabeledTextInput:
            id: meaning_input
            label_text: "meaning:"
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'top'
            Label:
                id: warning_label
                color: 'red'
                text: ''

        FocusButton:
            id: confirm_button
            text: 'CREATE NEW SYMBOL'
            size_hint: 1, None
            font_size: '20sp'
            height: self.texture_size[1] * 2.2
            on_press: root.confirm()
''')


class AbcScreen(Screen):
    abc = None
    symbols = []

    def update_abc(self, abc=None):
        if abc:
            self.abc = abc
        if not self.abc:
            return
        symbols_list = self.ids['symbols_list']
        symbols_list.clear_widgets()
        for symbol in self.abc.symbols:
            b = SymbolButton(symbol=symbol)
            symbols_list.add_widget(b)
        self.ids['header'].title = self.abc.name

    def show_create_new_symbol(self):
        NewSymbolPopup().open()

    def open_dir(self):
        platform.open_dir(self.abc.info_path, select=True)


class SymbolButton(DrawingButton):
    def __init__(self, **kwargs):
        self.symbol = kwargs.pop('symbol', None)
        if self.symbol:
            kwargs['text'] = self.symbol.name
            kwargs['drawing'] = self.symbol.random_drawing()
        super().__init__(**kwargs)

    def on_press(self):
        App.get_running_app().goto_symbol(self.symbol)


class NewSymbolPopup(Popup):
    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        super().__init__(**kwargs)
        self.symbol = None

    def on_confirm(self):
        pass

    def confirm(self):
        missing = []
        name = self.ids['name_input'].text
        meaning = self.ids['meaning_input'].text
        if not name:
            missing.append('name')
        if not meaning:
            missing.append('meaning')
        if missing:
            msg = "missing required input: %s" % ", ".join(missing)
            self.ids['warning_label'].text = msg
        else:
            self.symbol = TexnoMagicSymbol(name=name, meaning=meaning)
            self.dispatch('on_confirm')
            self.dismiss()
