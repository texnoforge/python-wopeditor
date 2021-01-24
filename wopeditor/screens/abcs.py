from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class AbcsScreen(Screen):
    abcs = []

    def update_abcs(self, abcs=None):
        if abcs:
            self.abcs = abcs
        abcs_list = self.ids['abcs_list']
        for abc in abcs:
            b = AbcButton(abc=abc)
            abcs_list.add_widget(b)


class AbcButton(Button):
    def __init__(self, **kwargs):
        self.abc = kwargs.pop('abc', None)
        if self.abc:
            kwargs['text'] = self.abc.name
        super().__init__(**kwargs)