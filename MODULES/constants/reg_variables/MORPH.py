from pymorphy3 import MorphAnalyzer
from typing import Final


MORPH: Final[MorphAnalyzer] = MorphAnalyzer(lang='ru')
