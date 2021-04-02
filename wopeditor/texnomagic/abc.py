import json
import os

from wopeditor.texnomagic import common 
from wopeditor.texnomagic.symbol import TexnoMagicSymbol


class TexnoMagicAlphabet:
    def __init__(self, name=None, base_path=None):
        self.name = name
        self.base_path = base_path
        self._symbols = None

    @property
    def info_path(self):
        return self.base_path / 'texno_alphabet.json'

    @property
    def symbols_path(self):
        return self.base_path / 'symbols'

    def load(self, base_path=None):
        if base_path:
            self.base_path = base_path

        assert self.base_path
        info = json.load(self.info_path.open())

        name = info.get('name')
        if not name:
            name = self.base_path.name
        self.name = name

        return self

    def load_symbols(self):
        self._symbols = []
        for symbol_info_path in self.symbols_path.glob('*/texno_symbol.json'):
            symbol = TexnoMagicSymbol()
            symbol.load(symbol_info_path.parent)
            self._symbols.append(symbol)

    def save(self):
        os.makedirs(self.base_path, exist_ok=True)
        info = {
            'name': self.name,
        }
        return json.dump(info, self.info_path.open('w'))

    def save_new_symbol(self, symbol):
        assert symbol.name

        if self._symbols is None:
            self.load_symbols()

        symbol.base_path = self.symbols_path / common.name2fn(symbol.name)
        symbol.save()
        return self._symbols.insert(0, symbol)

    @property
    def symbols(self):
        if self._symbols is None:
            self.load_symbols()
        return self._symbols