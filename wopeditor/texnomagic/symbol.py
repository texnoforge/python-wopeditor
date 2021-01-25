from wopeditor.texnomagic.drawing import TexnoMagicDrawing


class TexnoMagicSymbol:
    name = None
    base_path = None
    _drawings = None

    def load(self, base_path=None):
        if base_path:
            self.base_path = base_path
        self.name = self.base_path.name
        return self

    def load_drawings(self):
        self._drawings = []
        for drawing_path in self.base_path.glob('drawings/*'):
            drawing = TexnoMagicDrawing()
            drawing.load(drawing_path)
            self._drawings.append(drawing)

    @property
    def drawings(self):
        if self._drawings is None:
            self.load_drawings()
        return self._drawings