import json

from wopeditor.texnomagic.drawing import TexnoMagicDrawing
import os


class TexnoMagicSymbol:
    def __init__(self, name=None, meaning=None, base_path=None):
        self.name = name
        self.meaning = meaning
        self.base_path = base_path
        self._drawings = None

    @property
    def info_path(self):
        return self.base_path / 'texno_symbol.json'

    def load(self, base_path=None):
        if base_path:
            self.base_path = base_path
        
        assert base_path
        info = json.load(self.info_path.open())

        name = info.get('name')
        if not name:
            name = self.base_path.name
        self.name = name
        self.meaning = info.get('meaning')

        return self

    def load_drawings(self):
        self._drawings = []
        for drawing_path in self.base_path.glob('drawings/*'):
            drawing = TexnoMagicDrawing()
            drawing.load(drawing_path)
            self._drawings.append(drawing)

    def save(self):
        os.makedirs(self.base_path, exist_ok=True)
        info = {
            'name': self.name,
            'meaning': self.meaning,
        }
        return json.dump(info, self.info_path.open('w'))

    @property
    def drawings(self):
        if self._drawings is None:
            self.load_drawings()
        return self._drawings

    def __repr__(self):
        return 'TexnoMagicSymbol %s (%s) @ %s' % (self.name, self.meaning, self.base_path)