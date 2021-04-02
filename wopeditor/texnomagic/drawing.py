import csv


class TexnoMagicDrawing:

    def __init__(self, path=None, curves=None, points_range=1000.0):
        self.path = path
        self.points_range = points_range
        self._curves = curves

    @property
    def curves(self):
        if self._curves is None:
            self.load_curves()
        return self._curves

    @property
    def name(self):
        if self.path:
            return self.path.name
        return None

    def load(self, path=None):
        if path:
            self.path = path
        return self

    def load_curves(self):
        self._curves = []
        curve = []
        with self.path.open('r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row is None or '' in row:
                    self._curves.append(curve)
                    curve = []
                    continue
                curve.append(list(map(float, row)))
        self._curves.append(curve)

    def curves_fit_area(self, pos, size):
        k = min(*size) / self.points_range
        max_range = self.points_range * k
        x_offset = pos[0] + (size[0] - max_range) / 2
        y_offset = pos[1] + (size[1] - max_range) / 2

        def scale_point(point):
            return [x_offset + point[0] * k,
                    y_offset + point[1] * k]

        scurves = []
        for curve in self.curves:
            scurve = list(map(scale_point, curve))
            scurves.append(scurve)
        return scurves

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open('w', newline='') as f:
            writer = csv.writer(f)
            first = True
            for curve in self.curves:
                if first:
                    first = False
                else:
                    writer.writerow([None, None])
                writer.writerows(curve)

