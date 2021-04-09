import numpy as np
import pickle

from sklearn import mixture

# TODO: fix in PyInstaller upstream
# hidden import for PyInstaller
import sklearn.utils._weight_vector


class TexnoMagicSymbolModel:

    def __init__(self, path=None, n_gauss=10):
        self.path = path
        self.n_gauss = n_gauss
        self.gmm = None

    @property
    def data_path(self):
        if self.path:
            return self.path / 'model.gmm'
        return None

    def train(self, data, n_gauss=None):
        if n_gauss:
            self.n_gauss = n_gauss
        # thanks scikit-learn <3
        self.gmm = mixture.GaussianMixture(n_components=self.n_gauss)
        if data is None:
            return
        self.gmm.fit(data)

    def load(self, path=None):
        if path:
            self.path = path

        gmm_path = self.data_path
        if gmm_path.exists():
            try:
                self.gmm = pickle.load(gmm_path.open('rb'))
                self.n_gauss = self.gmm.n_components
            except Exception:
                print("MODEL: load FAIL: %s " % gmm_path)

    def save(self):
        self.path.mkdir(parents=True, exist_ok=True)
        pickle.dump(self.gmm, self.data_path.open('wb'))

    def __repr__(self):
        return '<TexnoMagicSymbolModel @ %s>' % self.path
