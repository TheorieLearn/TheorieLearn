from typing import List

from nltk.grammar import CFG
from nltk.tree import Tree

class RecursiveDescentParser:
    def __init__(self, grammar: CFG, trace: int = 0): ...
    def parse_all(self, sent: List[str]) -> List[Tree]: ...
