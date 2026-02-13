"""Exception classes for regular expression parsing and lexing."""

from dataclasses import dataclass


class RegexException(Exception):
    """The base class for all automaton-related errors."""

    pass


class InvalidTokenOrdering(RegexException):
    """An exception related to an invalid ordering of tokens."""

    pass


class InvalidVariableDefinition(RegexException):
    """An exception related to an invalid definition of a variable."""

    pass


class ParserException(RegexException):
    """An exception related to an error when parsing."""

    pass


@dataclass
class LexerException(RegexException):
    """An exception raised for issues in lexing"""

    message: str
    position: int
