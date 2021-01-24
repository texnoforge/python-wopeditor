import csv


class TexnoMagicDrawing:
    name = None
    path = None
    _curves = None

    def load(self, path=None):
        if path:
            self.path = path
        self.name = self.path.name
        return self

    def load_curves(self):
        self._curves = []
        with self.path.openc('r') as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)

    @property
    def curves(self):
        if self._cureves is None:
            self.load_curves()
        return self._curves