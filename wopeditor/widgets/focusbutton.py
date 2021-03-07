from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.button import Button


Builder.load_string('''
<FocusButton>:
    bold: self.focus
''')


class FocusButton(FocusBehavior, Button):
    def keyboard_on_key_up(self, window, keycode):
        super().keyboard_on_key_up(window, keycode)
        if keycode[1] in ['enter', 'numpadenter']:
            self.dispatch("on_release")
            return True
        return False