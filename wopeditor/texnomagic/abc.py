from texnomagic.symbol import TexnoMagicSymbol


class TexnoMagicAlphabet:
    name = None
    base_path = None
    _symbols = None

    def load(self, base_path=None):
        if base_path:
            self.base_path = base_path

        self.name = self.base_path.name
        return self

    def load_symbols(self):
        self._symbols = {}
        for symbol_info_path in self.base_path.glob('symbols/*/texno_symbol.json'):
            symbol = TexnoMagicSymbol()
            symbol.load(symbol_info_path.parent)
            self._symbols[symbol.name] = symbol

    @property
    def symbols(self):
        if self._symbols is None:
            self.load_symbols()
        return self._symbols