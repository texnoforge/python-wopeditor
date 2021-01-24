
import glob
from pathlib import Path

from texnomagic.abc import TexnoMagicAlphabet


def get_alphabets(base_path):
    abcs = []
    for abc_info_path in base_path.glob('*/texno_alphabet.json'):
        abc = TexnoMagicAlphabet()
        abc.load(abc_info_path.parent)
        abcs.append(abc)
    return abcs
