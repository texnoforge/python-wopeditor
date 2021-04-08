from kivy.graphics import Color, Ellipse, Line, PushMatrix, PopMatrix, Rotate, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang import Builder

import numpy as np


class ModelPreview(Button):
    symbol = None

    def __init__(self, **kwargs):
        symbol = kwargs.pop('symbol', None)
        super().__init__(**kwargs)
        if symbol:
            self.update_symbol(symbol=symbol)
        self.bind(size=self.update_symbol,
                  pos=self.update_symbol)

    def update_symbol(self, *args, symbol=None):
        if symbol:
            self.symbol = symbol

        self.canvas.clear()

        if not self.symbol:
            return

        asize = np.array(self.size)
        padding =  0.1
        ioffset = padding * asize
        isize = asize * (1 - 2 * padding)
        slen = min(isize)
        offset = ioffset + (isize - slen) / 2
        ssize = np.array([slen, slen])
        ipos = self.pos + ioffset
        spos = self.pos + offset

        model = self.symbol.model
        with self.canvas:
            Color(0.05, 0.05, 0.05)
            #Rectangle(pos=self.pos, size=self.size)
            Rectangle(pos=spos, size=ssize)

            if model and hasattr(model.gmm, 'means_'):
                Color(1, 0.1, 0.0, 0.8)
                means = model.gmm.means_
                # draw covariances for each Gaussian
                for i, cov in enumerate(self.symbol.model.gmm.covariances_):
                    v, w = np.linalg.eigh(cov)
                    u = w[0] / np.linalg.norm(w[0])
                    angle = np.arctan2(u[1], u[0])
                    angle = 180 * angle / np.pi  # convert to degrees
                    v = 2. * np.sqrt(2.) * np.sqrt(v)
                    center = (means[i, :2] / 1000) * slen + spos
                    size = (v / 1000) * slen
                    pos = center - (size / 2)
                    # numpy example
                    # ell = mpl.patches.Ellipse(means[i, :2], v[0], v[1],
                    #                     180 + angle, color=color)
                    PushMatrix()
                    Rotate(origin=center, angle=angle)
                    Ellipse(
                        pos=pos,
                        size=size,
                    )
                    PopMatrix()

            # draw all symbol drawings
            Color(0.7, 0.7, 0.0, 0.2)
            for drawing in self.symbol.drawings:
                for curve in drawing.curves_fit_area(ipos, isize):
                    Line(points=curve.tolist())
