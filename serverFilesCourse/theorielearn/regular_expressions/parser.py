from __future__ import annotations

import re
from itertools import count, zip_longest
from typing import AbstractSet, Dict, List, Optional, Set, Type

import theorielearn.regular_expressions.exceptions as exceptions
import theorielearn.regular_expressions.postfix as postfix
from automata.base.automaton import AutomatonStateT
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from theorielearn.regular_expressions.lexer import Lexer, Token

BuilderTransitionsT = Dict[int, Dict[str, Set[int]]]


class NFARegexBuilder:
    """Builder class designed for speed in parsing regular expressions into NFAs."""

    __slots__ = ["_transitions", "_initial_state", "_final_states", "_consumed"]
    _state_name_counter = count(0)

    _transitions: BuilderTransitionsT
    _initial_state: AutomatonStateT
    _final_states: Set[AutomatonStateT]
    _consumed: bool

    def __init__(
        self,
        *,
        transitions: BuilderTransitionsT,
        initial_state: AutomatonStateT,
        final_states: AbstractSet[AutomatonStateT],
    ) -> None:
        """
        Initialize new builder class and remap state names.
        """

        state_map = {
            original_state: self.__get_next_state_name()
            for original_state in transitions
        }

        self._initial_state = state_map[initial_state]
        self._final_states = {state_map[state] for state in final_states}

        self._transitions = {
            state_map[start_state]: {
                chr: {state_map[dest_state] for dest_state in dest_set}
                for chr, dest_set in transition.items()
            }
            for start_state, transition in transitions.items()
        }

        self._consumed = False

    @classmethod
    def from_dfa(cls: Type[NFARegexBuilder], dfa: DFA) -> NFARegexBuilder:
        """
        Initialize this builder with a DFA.
        """

        new_transitions: BuilderTransitionsT = {
            int(start_state): {
                input_symbol: {end_state}
                for input_symbol, end_state in transition.items()
            }
            for start_state, transition in dfa.transitions.items()
        }

        return cls(
            transitions=new_transitions,
            initial_state=dfa.initial_state,
            final_states=dfa.final_states,
        )

    @classmethod
    def from_string_literal(
        cls: Type[NFARegexBuilder], literal: str
    ) -> NFARegexBuilder:
        """
        Initialize this builder accepting only the given string literal.
        """

        transitions: BuilderTransitionsT = {
            i: {chr: {i + 1}} for i, chr in enumerate(literal)
        }

        final_state = len(literal)
        transitions[final_state] = dict()

        return cls(transitions=transitions, initial_state=0, final_states={final_state})

    def union(self, other: NFARegexBuilder) -> None:
        """
        Apply the union operation to the NFA represented by this builder and other.
        """
        self.__check_consumed()
        other.__consume()

        self._transitions.update(other._transitions)

        new_initial_state = self.__get_next_state_name()

        # Add epsilon transitions from new start state to old ones
        self._transitions[new_initial_state] = {
            "": {self._initial_state, other._initial_state}
        }

        self._initial_state = new_initial_state
        self._final_states.update(other._final_states)

    def concatenate(self, other: NFARegexBuilder) -> None:
        """
        Apply the concatenate operation to the NFA represented by this builder
        and other.
        """
        self.__check_consumed()
        other.__consume()

        self._transitions.update(other._transitions)

        for state in self._final_states:
            self._transitions[state].setdefault("", set()).add(other._initial_state)

        self._final_states = other._final_states

    def kleene_star(self) -> None:
        """
        Apply the kleene star operation to the NFA represented by this builder.
        """
        self.__check_consumed()

        new_initial_state = self.__get_next_state_name()

        self._transitions[new_initial_state] = {"": {self._initial_state}}

        for state in self._final_states:
            self._transitions[state].setdefault("", set()).add(self._initial_state)

        self._initial_state = new_initial_state
        self._final_states.add(new_initial_state)

    def copy(self) -> NFARegexBuilder:
        """Make and return a copy of this builder."""
        self.__check_consumed()

        return NFARegexBuilder(
            transitions=self._transitions,
            initial_state=self._initial_state,
            final_states=self._final_states,
        )

    def build(self, input_symbols: AbstractSet[str]) -> NFA:
        """Construct an NFA object equivalent to this one."""
        self.__check_consumed()

        return NFA(
            states=set(self._transitions.keys()),
            input_symbols=input_symbols,
            transitions=self._transitions,
            initial_state=self._initial_state,
            final_states=self._final_states,
        )

    def __consume(self) -> None:
        """Mark self as consumed."""
        self.__check_consumed()
        self._consumed = True

    def __check_consumed(self) -> None:
        """Raise exception if self is already consumed."""
        if self._consumed:
            raise exceptions.ParserException(
                "This NFARegexBuilder class has already been consumed."
            )

    @classmethod
    def __get_next_state_name(cls: Type[NFARegexBuilder]) -> int:
        """Get next int for use as a state name (to avoid naming conflicts)."""
        return next(cls._state_name_counter)


class UnionToken(postfix.InfixOperator[NFARegexBuilder]):
    """Subclass of infix operator defining the union operator."""

    def get_precedence(self) -> int:
        return 1

    def op(self, left: NFARegexBuilder, right: NFARegexBuilder) -> NFARegexBuilder:
        left.union(right)
        return left


class KleeneToken(postfix.PostfixOperator[NFARegexBuilder]):
    """Subclass of postfix operator defining the kleene star operator."""

    def get_precedence(self) -> int:
        return 3

    def op(self, left: NFARegexBuilder) -> NFARegexBuilder:
        left.kleene_star()
        return left


class ConcatToken(postfix.InfixOperator[NFARegexBuilder]):
    """Subclass of infix operator defining the concatenation operator."""

    def get_precedence(self) -> int:
        return 2

    def op(self, left: NFARegexBuilder, right: NFARegexBuilder) -> NFARegexBuilder:
        left.concatenate(right)
        return left


class StringToken(postfix.Literal[NFARegexBuilder]):
    """Subclass of literal token defining a string literal."""

    def val(self) -> NFARegexBuilder:
        return NFARegexBuilder.from_string_literal(self.text)


class VariableToken(postfix.Literal[NFARegexBuilder]):
    """Subclass of literal token representing a variable."""

    __slots__ = ["_equiv_nfa"]

    _equiv_nfa: Optional[NFARegexBuilder]

    def __init__(self, text: str, equiv_nfa: NFARegexBuilder) -> None:
        self.text = text
        self._equiv_nfa = equiv_nfa

    def val(self) -> NFARegexBuilder:
        if self._equiv_nfa is None:
            raise exceptions.ParserException(
                f"Token {self.__repr__()} has no data (already returned)."
            )

        res = self._equiv_nfa
        self._equiv_nfa = None
        return res


def add_concat_tokens(
    token_list: List[Token[NFARegexBuilder]],
) -> List[Token[NFARegexBuilder]]:
    """Add concat tokens to list of parsed infix tokens."""

    final_token_list = []
    concat_pairs = [
        (postfix.Literal, postfix.Literal),
        (postfix.RightParen, postfix.LeftParen),
        (postfix.RightParen, postfix.Literal),
        (postfix.Literal, postfix.LeftParen),
        (postfix.PostfixOperator, postfix.Literal),
        (postfix.PostfixOperator, postfix.LeftParen),
    ]

    for curr_token, next_token in zip_longest(token_list, token_list[1:]):
        final_token_list.append(curr_token)

        if next_token:
            for firstClass, secondClass in concat_pairs:
                if isinstance(curr_token, firstClass) and isinstance(
                    next_token, secondClass
                ):
                    final_token_list.append(ConcatToken("."))

    return final_token_list


def bind_kleene_star_to_literal(
    token_list: List[Token[NFARegexBuilder]],
) -> List[Token[NFARegexBuilder]]:
    """Bind kleene star to last characters in literals."""

    final_token_list: List[Token[NFARegexBuilder]] = []

    for curr_token, next_token in zip_longest(token_list, token_list[1:]):
        if (
            isinstance(curr_token, StringToken)
            and isinstance(next_token, KleeneToken)
            and len(curr_token.text) > 1
        ):
            text = curr_token.text[:-1]
            end = curr_token.text[-1]
            final_token_list.extend([StringToken(text), StringToken(end)])
        else:
            final_token_list.append(curr_token)

    return final_token_list


SubsDictT = Dict[str, NFARegexBuilder]


def compute_nfa_from_regex_lines(
    regex: str, alphabet: AbstractSet[str] = {"0", "1"}
) -> NFA:
    """Computes an NFA from a multi-line regex statement."""

    # Remove blank lines
    regex_lines = [line for line in regex.splitlines() if line.replace(" ", "")]

    if not regex_lines:
        raise exceptions.RegexException("Cannot parse blank regular expression.")

    *all_but_last_line, last_line = regex_lines

    subs_dict: SubsDictT = {"e": NFARegexBuilder.from_string_literal("")}
    line_pattern = re.compile(r"\s*([A-Za-z]+)\s*=(.*)")

    for regex_line in all_but_last_line:
        line_match = line_pattern.match(regex_line)

        if line_match is None:
            raise exceptions.InvalidVariableDefinition(
                f"Invalid variable assignment in line '{regex_line}'"
            )

        variable_name = line_match[1]
        regex_statement = line_match[2]

        # For subexpression, minimize NFA for re-use later
        nfa = parse_regex_line(regex_statement, subs_dict, alphabet).build(alphabet)
        subs_dict[variable_name] = NFARegexBuilder.from_dfa(
            DFA.from_nfa(nfa, retain_names=False, minify=True).to_complete()
        )
    return parse_regex_line(last_line, subs_dict, alphabet).build(alphabet)


def parse_regex_line(
    regexstr: str, subs_dict: SubsDictT, alphabet: AbstractSet[str]
) -> NFARegexBuilder:
    """Return an NFARegexBuilder corresponding to regexstr using subs_dict for variable substitutions."""

    lexer: Lexer[NFARegexBuilder] = Lexer()

    lexer.register_token(postfix.LeftParen, r"\(")
    lexer.register_token(postfix.RightParen, r"\)")
    lexer.register_token(StringToken, rf"[{''.join(alphabet)}]+")
    lexer.register_token(UnionToken, r"\+")
    lexer.register_token(KleeneToken, r"\*")
    lexer.register_token(ConcatToken, r"\.")

    def variable_factory(text: str) -> VariableToken:
        if text not in subs_dict:
            raise exceptions.InvalidVariableDefinition(
                f"Invalid variable name '{text}'"
            )
        return VariableToken(text, subs_dict[text].copy())

    lexer.register_token(variable_factory, r"[A-Za-z]+")

    lexed_tokens = lexer.lex(regexstr)

    try:
        postfix.validate_tokens(lexed_tokens)
    except exceptions.InvalidTokenOrdering as e:
        raise exceptions.InvalidTokenOrdering(f"'{regexstr}': {e}")

    kleene_bound_tokens = bind_kleene_star_to_literal(lexed_tokens)
    tokens_with_concats = add_concat_tokens(kleene_bound_tokens)
    postfix_tokens: List[Token[NFARegexBuilder]] = postfix.tokens_to_postfix(
        tokens_with_concats
    )

    return postfix.parse_postfix_tokens(postfix_tokens)
