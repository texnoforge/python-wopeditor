from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup

from wopeditor.texnomagic import common
from wopeditor.texnomagic.abc import TexnoMagicAlphabet


class AbcsScreen(Screen):
    abcs = []

    def update_abcs(self, abcs=None):
        if abcs:
            self.abcs = abcs
        if not self.abcs:
            return
        abcs_lists = self.ids['abcs_lists']
        abcs_lists.clear_widgets()
        for tag, abcs in self.abcs.abcs.items():
            if not abcs:
                continue

            list_id = "%s_abcs_list" % tag
            abcs_list = StackLayout(
                size_hint=(1,None),
                spacing=5)

            for abc in abcs:
                b = AbcButton(abc=abc)
                abcs_list.add_widget(b)

            abcs_lists.add_widget(abcs_list)
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