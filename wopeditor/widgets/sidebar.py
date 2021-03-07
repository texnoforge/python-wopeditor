from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


Builder.load_string('''
<Sidebar>:
    orientation: 'vertical'
    padding: 0, 0, 30, 0
    size_hint_x: None
    width: 200
    spacing: 5

<SideButton>:
    size_hint: None, None
    height: 40
''')


class Sidebar(BoxLayout):
    pass


class SideButton(Button):
    pass