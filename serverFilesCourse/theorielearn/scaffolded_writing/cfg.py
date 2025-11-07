import html
import json
from typing import Dict, List, Set, Union

from nltk.grammar import CFG, Nonterminal, Production

TerminalT = str
SymbolT = Union[Nonterminal, TerminalT]


class ScaffoldedWritingCFG(CFG):
    def __init__(self, start: Nonterminal, productions: List[Production]) -> None:
        super().__init__(start, productions)

        lhs_nonterminals = {prod.lhs() for prod in self.productions()}
        rhs_nonterminals = {
            symbol
            for prod in self.productions()
            for symbol in prod.rhs()
            if isinstance(symbol, Nonterminal)
        }

        nonterminals_missing_from_lhs = rhs_nonterminals - lhs_nonterminals
        if nonterminals_missing_from_lhs:
            raise Exception(
                f"These nonterminals never appear on the LHS of a production rule: {nonterminals_missing_from_lhs}"
            )

        nonterminals_missing_from_rhs = (
            lhs_nonterminals - {self.start()} - rhs_nonterminals
        )
        if nonterminals_missing_from_rhs:
            raise Exception(
                f"These nonterminals never appear on the RHS of a production rule: {nonterminals_missing_from_rhs}"
            )

        self.nonterminals = lhs_nonterminals

        self.terminals = {
            symbol
            for prod in self.productions()
            for symbol in prod.rhs()
            if isinstance(symbol, TerminalT)
        }

        # Maps each nonterminal to the set of terminal and nonterminal symbols that
        # it can *directly* produce in one step.
        self.symbols_produced_by_nonterminal: Dict[Nonterminal, Set[SymbolT]] = {
            nonterminal: set() for nonterminal in self.nonterminals
        }

        for prod in self.productions():
            self.symbols_produced_by_nonterminal[prod.lhs()].update(prod.rhs())

    def to_json_string(self) -> str:
        cfg_as_json = {
            "start": html.escape(self.start().symbol()),
            "productions": [
                {
                    "lhs": html.escape(prod.lhs().symbol()),
                    "rhs": [
                        {
                            "text": html.escape(str(symbol)),
                            "isTerminal": isinstance(symbol, TerminalT),
                        }
                        for symbol in prod.rhs()
                    ],
                }
                for prod in self.productions()
            ],
        }

        return json.dumps(cfg_as_json)

    def can_produce_path(self, *path: str) -> bool:
        """
        Determines whether or not the CFG can produce a parse tree that contains the specified path.
        Note that this is a global property of the CFG; it is not a property of a specific submission's parse tree.
        """
        assert len(path) > 0

        if len(path) == 1:
            symbol = path[0]
            return symbol in self.terminals or Nonterminal(symbol) in self.nonterminals

        def can_parent_produce_child(parent: str, child: str) -> bool:
            if Nonterminal(parent) not in self.nonterminals:
                return False

            allowed_children = self.symbols_produced_by_nonterminal[Nonterminal(parent)]
            return child in allowed_children or Nonterminal(child) in allowed_children

        return all(
            can_parent_produce_child(parent, child)
            for parent, child in zip(path[:-1], path[1:])
        )
