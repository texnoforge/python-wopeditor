from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
<LabeledTextInput>:
    label_text: 'label'
    text: text_input.text
    spacing: 10
    size_hint: 1, None
    height: text_input.height

    Label:
        size_hint_x: 0.5
        text: root.label_text
        text_size: self.size
        halign: 'right'
        valign: 'center'

    AnchorLayout:
        anchor_y: 'center'
        TextInput:
            id: text_input
            size_hint: 1, None
            height: self.font_size * 2
            multiline: False
            write_tab: False
''')


class LabeledTextInput(BoxLayout):
    pass