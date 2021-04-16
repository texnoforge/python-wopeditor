from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.popup import Popup



Builder.load_string('''
<ErrorPopup>:
    title: ":("
    text: "oh noes"
    size_hint: None, None
    size: 400, 200
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: root.text
        Button:
            text: 'OK'
            size_hint_y: None
            height: dp(50)
            on_press: root.dismiss()
''')


class ErrorPopup(Popup):
    text = StringProperty()
