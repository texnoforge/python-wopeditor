import json
import os
from pathlib import Path
import shutil

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
        self.sort_symbols()

    def sort_symbols(self):
        if not self._symbols:
            return
        known = []
        for core_symbol in common.CORE_SYMBOLS_ORDER:
            for symbol in self._symbols:
                if symbol.meaning == core_symbol:
                    known.append(symbol)
                    self._symbols.remove(symbol)
                    break
        self._symbols = known + self._symbols

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

    def export(self, out_path=None):
        """
        export alphabet into a zipfile
        """
        if not out_path:
            out_path = common.EXPORT_PATH

        ar_fn = self.base_path.name
        out_fn = out_path / ar_fn
        return shutil.make_archive(
            out_fn, 'zip',
            root_dir=self.base_path.parent,
            base_dir=self.base_path.name,
        )

    @property
    def symbols(self):
        if self._symbols is None:
            self.load_symbols()
        return self._symbols
