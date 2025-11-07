"""Tests of the postfix conversion and parsing utility functions."""

from typing import List

import pytest
import theorielearn.regular_expressions.postfix as postfix
from theorielearn.regular_expressions.lexer import Lexer, Token


class Integer(postfix.Literal[int]):
    def val(self) -> int:
        """It evaluates to its (integer) value."""
        return int(self.text)


class Add(postfix.InfixOperator[int]):
    """Addition."""

    def get_precedence(self) -> int:
        return 10  # Precedence: higher than integers, lower than mult

    def op(self, left: int, right: int) -> int:
        return left + right


class Minus(postfix.InfixOperator[int]):
    """Subtraction."""

    def get_precedence(self) -> int:
        return 10  # Precedence: higher than integers, lower than mult

    def op(self, left: int, right: int) -> int:
        return left - right


class Mult(postfix.InfixOperator[int]):
    """Multiplication."""

    def get_precedence(self) -> int:
        return 20  # Higher precedence than addition/substraction.

    def op(self, left: int, right: int) -> int:
        return left * right


class Divide(postfix.InfixOperator[int]):
    """Division."""

    def get_precedence(self) -> int:
        return 20  # Same precedence than multiplication

    def op(self, left: int, right: int) -> int:
        return left // right


@pytest.fixture
def arithmetic_lexer() -> Lexer[int]:
    l: Lexer[int] = Lexer()

    l.register_token(postfix.LeftParen, r"\(")
    l.register_token(postfix.RightParen, r"\)")
    l.register_token(Integer, r"[0-9]+")
    l.register_token(Add, r"\+")
    l.register_token(Minus, r"-")
    l.register_token(Mult, r"\*")
    l.register_token(Divide, r"/")

    return l


def verify_nested_parenthesized_expression() -> None:
    # Parsing:
    # "( 4 + ( 1 + 2 * 3 * ( 4 + 5 ) + 6 ) ) * 7 + 8"
    tokens: List[Token[int]] = [
        postfix.LeftParen("("),
        Integer("4"),
        Add("+"),
        postfix.LeftParen("("),
        Integer("1"),
        Add("+"),
        Integer("2"),
        Mult("*"),
        Integer("3"),
        Mult("*"),
        postfix.LeftParen("("),
        Integer("4"),
        Add("+"),
        Integer("5"),
        postfix.RightParen(")"),
        Add("+"),
        Integer("6"),
        postfix.RightParen(")"),
        postfix.RightParen(")"),
        Mult("*"),
        Integer("7"),
        Add("+"),
        Integer("8"),
    ]

    postfix_tokens: List[Token[int]] = postfix.tokens_to_postfix(tokens)
    res = postfix.parse_postfix_tokens(postfix_tokens)
    assert (4 + (1 + 2 * 3 * (4 + 5) + 6)) * 7 + 8 == res


@pytest.mark.parametrize(
    "statement", ["+6", "+5+", "6/", "1 + 2 - + 3", ")(", "(((2))", "(+5", "6/)"]
)
def verify_expression_invalid_ordering(statement, arithmetic_lexer: Lexer[int]) -> None:
    with pytest.raises(postfix.InvalidTokenOrdering):
        postfix.validate_tokens(arithmetic_lexer.lex(statement))


class VerifyArithmeticParser:
    """Test parsing arithmetic expressions."""

    def parse(self, tokens: List[Token[int]]) -> int:
        postfix_tokens = postfix.tokens_to_postfix(tokens)
        return postfix.parse_postfix_tokens(postfix_tokens)

    def verify_single_number(self, arithmetic_lexer: Lexer[int]) -> None:
        val = self.parse(arithmetic_lexer.lex("13"))
        assert 13 == val

    def verify_negative_number(self, arithmetic_lexer: Lexer[int]) -> None:
        val = self.parse(arithmetic_lexer.lex("0-13"))
        assert -13 == val

    def verify_simple_mult(self, arithmetic_lexer: Lexer[int]) -> None:
        assert 8 == self.parse(arithmetic_lexer.lex("2 * 4"))
        assert 8 == self.parse(arithmetic_lexer.lex("2 * 2 * 2"))
        assert 8 == self.parse(arithmetic_lexer.lex("2 * (2 * 2)"))
        assert 8 == self.parse(arithmetic_lexer.lex("(2 * 2) * 2"))
        assert 8 == self.parse(arithmetic_lexer.lex("(2 + 2) * 2"))

    def verify_precedence(self, arithmetic_lexer: Lexer[int]) -> None:
        assert 8 == self.parse(arithmetic_lexer.lex("2 * 3 + 2"))
        assert 10 == self.parse(arithmetic_lexer.lex("2 * (3+2)"))

    def verify_negative_mult(self, arithmetic_lexer: Lexer[int]) -> None:
        assert 8 == self.parse(arithmetic_lexer.lex("(0-2) * (0- 4)"))
        assert 8 == self.parse(arithmetic_lexer.lex("(0-2) * 2 * (0-2)"))
        assert -5 == self.parse(arithmetic_lexer.lex("1 + (0-2) * 3"))

    def verify_division(self, arithmetic_lexer: Lexer[int]) -> None:
        assert 2 == self.parse(arithmetic_lexer.lex("4 / 2"))
        assert 2 == self.parse(arithmetic_lexer.lex("5 / 2"))
        assert 2 == self.parse(arithmetic_lexer.lex("6 - 8 / 2"))
        assert 3 == self.parse(arithmetic_lexer.lex("3 * 2 / 2"))
        assert 3 == self.parse(arithmetic_lexer.lex("2 * 3 / 2"))
        assert 8 == self.parse(arithmetic_lexer.lex("8 / 2 * 2"))
        assert 8 == self.parse(arithmetic_lexer.lex("(8 / 2) * 2"))
        assert 2 == self.parse(arithmetic_lexer.lex("8 / (2 * 2)"))
        assert 2 == self.parse(arithmetic_lexer.lex("16/4/2"))
