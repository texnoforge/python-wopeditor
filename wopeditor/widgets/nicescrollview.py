from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button


Builder.load_string('''
<NiceScrollView>:
    do_scroll_x: False
    do_scroll_y: True
    bar_pos_y: "right"
''')


class NiceScrollView(ScrollView):
    pass
