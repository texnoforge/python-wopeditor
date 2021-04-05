from kivy.factory import Factory
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup

from wopeditor.texnomagic import common
from wopeditor.texnomagic.abc import TexnoMagicAlphabet

from wopeditor.widgets.header import Header
from wopeditor.widgets.nicescrollview import NiceScrollView


Builder.load_string('''
<AbcsScreen>:
    name: "abcs"

    GridLayout:
        cols: 1
        padding: [10, 0]

        Header:
            title: "alphabets"

        BoxLayout:
            Sidebar:
                id: sidebar
                SideButton:
                    text: "new alphabet"
                    on_release: root.show_create_new_abc()
                SideButton:
                    text: "open dir"
                    on_release: root.open_dir()
                SideButton:
                    text: "refresh"
                    on_release: app.refresh()
                FloatLayout:
                    #Filler

            NiceScrollView:
                id: main_scroll
                BoxLayout:
                    id: abcs_lists
                    size_hint_y: None
                    height: max(main_scroll.height, self.minimum_height)
                    orientation: 'vertical'


<AbcButton>:
    size_hint: None, None
    size: [self.texture_size[0] + dp(40), dp(72)]
    font_size: dp(36)
    on_release: app.goto_abc(self.abc)


<ModButton>:
    size: [340, 200]
    size_hint: None, None
    on_release: app.download_mod(self.mod)

    AsyncImage:
        id: bimg
        size: [320, 180]
        pos: [root.x + 10, root.y + 10]
    AnchorLayout:
        size: root.size
        pos: root.pos
        anchor_x: 'center'
        anchor_y: 'center'
        Label:
            id: blabel
            font_size: dp(36)


<NewAbcPopup>:
    size_hint: None, None
    width: 400
    height: name_input.height * 2 + confirm_button.height + self.title_size + dp(80)
    title: "create new alphabet"
    on_open: name_input.ids['text_input'].focus = True
    on_confirm: app.add_new_abc(self.abc)
    BoxLayout:
        id: content
        orientation: 'vertical'
        padding: [0, 5, 0, 0]
        spacing: 5
        LabeledTextInput:
            id: name_input
            label_text: "name:"
            focus: True
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'top'
            Label:
                id: warning_label
                color: 'red'
                text: ''

        FocusButton:
            id: confirm_button
            text: 'CREATE NEW ALPHABET'
            size_hint: 1, None
            font_size: '20sp'
            height: self.texture_size[1] * 2.2
            on_release: root.confirm()


<AbcsLabel@Label>:
    font_size: dp(24)
    size_hint: None, None
    size: self.texture_size


<AbcsLayout@StackLayout>:
    spacing: 5
    size_hint_y: None
    height: self.minimum_height
    padding: [0, 5]
''')


class AbcsScreen(Screen):
    abcs = []
    mods = None

    def update_abcs(self, abcs=None, mods=None):
        if abcs:
            self.abcs = abcs
        if mods:
            self.mods = mods
        if not self.abcs:
            return

        abcs_lists = self.ids['abcs_lists']
        abcs_lists.clear_widgets()
        for tag, abcs in self.abcs.abcs.items():
            if not abcs:
                continue
            abcs_label = Factory.AbcsLabel(text=tag)
            abcs_lists.add_widget(abcs_label)

            abcs_list = Factory.AbcsLayout()
            for abc in abcs:
                b = AbcButton(abc=abc)
                abcs_list.add_widget(b)
            abcs_lists.add_widget(abcs_list)

        if self.mods:
            mods_label = Factory.AbcsLabel(text="online community mods")
            abcs_lists.add_widget(mods_label)

            mods_list = Factory.AbcsLayout()
            for mod in self.mods:
                b = Factory.ModButton(mod=mod)
                mods_list.add_widget(b)
            abcs_lists.add_widget(mods_list)

        # filler
        abcs_lists.add_widget(BoxLayout())
        Logger.info("abcs: updated: %s", self.abcs)

    def show_create_new_abc(self):
        NewAbcPopup().open()

    def open_dir(self):
        p = self.abcs.paths.get('user', {})
        if not p:
            return
        if not p.exists():
            p.mkdir(parents=True)

        common.open_dir(p)


class AbcButton(Button):
    def __init__(self, **kwargs):
        self.abc = kwargs.pop('abc', None)
        if self.abc:
            kwargs['text'] = self.abc.name
        super().__init__(**kwargs)


class ModButton(Button):
    def __init__(self, **kwargs):
        self.mod = kwargs.pop('mod', None)
        if self.mod:
            kwargs['text'] = self.mod.name
        super().__init__(**kwargs)
        self.update()

    def update(self):
        if not self.mod:
            return
        self.ids['bimg'].source = self.mod.logo_url
        self.ids['blabel'].text = self.mod.name


class NewAbcPopup(Popup):
    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        super().__init__(**kwargs)
        self.abc = None

    def on_confirm(self):
        pass

    def confirm(self):
        missing = []
        name = self.ids['name_input'].text
        if not name:
            missing.append('name')
        if missing:
            msg = "missing required input: %s" % ", ".join(missing)
            self.ids['warning_label'].text = msg
        else:
            self.abc = TexnoMagicAlphabet(name=name)
            self.dispatch('on_confirm')
            self.dismiss()
