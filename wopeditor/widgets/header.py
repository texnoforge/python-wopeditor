from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_string('''
<Header>:
    size_hint: 1, None

    AnchorLayout:
        id: hdr_layout
        anchor_x: 'center'
        anchor_y: 'center'

        Label:
            id: hdr_label
            text: root.title
            background_color: 0.3, 1, 1, 1
            font_size: 48

    FloatLayout:
        size: 0, 0
        size_hint: None, None

        AnchorLayout:
            size: [hdr_layout.size[0], hdr_label.size[1]]
            size_hint: None, None
            pos: [self.parent.pos[0], hdr_label.pos[1]]
            anchor_x: 'left'
            anchor_y: 'center'

            Button:
                id: back
                text: "< back"
                size: self.texture_size[0] * 2, self.texture_size[1] * 2
                size_hint: None, None
                on_release: root.dispatch('on_press_back')
''')


class Header(RelativeLayout):
    title = StringProperty('title')

    def __init__(self, **kwargs):
        self.register_event_type('on_press_back')
        super().__init__(**kwargs)

    def on_press_back(self):
        pass
