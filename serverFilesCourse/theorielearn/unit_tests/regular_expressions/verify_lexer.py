"""Tests for lexer-related code."""

import pytest
from theorielearn.regular_expressions.lexer import Lexer, LexerException, TokenRegistry
from theorielearn.regular_expressions.postfix import LeftParen, RightParen, Token


def register_parens(lexer: Lexer) -> None:
    lexer.register_token(LeftParen, r"\(")
    lexer.register_token(RightParen, r"\)")


class VerifyTokenRegistryTestCase:
    def verify_add_token(self) -> None:
        class AToken(Token):
            pass

        class BToken(Token):
            pass

        registry: TokenRegistry = TokenRegistry()
        assert 0 == len(registry._tokens)

        registry.register(AToken, r"a+")
        assert 1 == len(registry._tokens)

        registry.register(BToken, r"b+")
        assert 2 == len(registry._tokens)

    def verify_get_matches_no_tokens_notext(self) -> None:
        registry: TokenRegistry = TokenRegistry()
        assert [] == list(registry.matching_tokens("", 0))

    def verify_get_matches_no_tokens_text(self) -> None:
        registry: TokenRegistry = TokenRegistry()
        assert [] == list(registry.matching_tokens("foo", 0))

    def verify_get_matches_notext(self) -> None:
        class AToken(Token):
            pass

        registry: TokenRegistry = TokenRegistry()
        registry.register(AToken, r"a")
        assert [] == list(registry.matching_tokens("", 0))

    def verify_get_matches(self) -> None:
        class AToken(Token):
            pass

        registry: TokenRegistry = TokenRegistry()
        registry.register(AToken, r"a")

        matches = list(registry.matching_tokens("aaa", 0))
        assert 1 == len(matches)
        assert isinstance(matches[0][0]("a"), AToken)

    def verify_multiple_matches(self) -> None:
        class AToken(Token):
            pass

        class AAToken(Token):
            pass

        registry: TokenRegistry = TokenRegistry()
        registry.register(AToken, r"a")
        registry.register(AAToken, r"aa")

        matches = list(registry.matching_tokens("aaa", 0))
        assert 2 == len(matches)
        assert isinstance(matches[0][0]("a"), AToken)
        assert isinstance(matches[1][0]("aa"), AAToken)

    def verify_get_token_multiple(self) -> None:
        class AToken(Token):
            pass

        class AAToken(Token):
            pass

        registry: TokenRegistry = TokenRegistry()
        registry.register(AToken, r"a")
        registry.register(AAToken, r"aa")

        match = registry.get_token("aaa")
        assert match is not None
        assert isinstance(match[0]("aa"), AAToken)

    def verify_get_token_multiple_inverted(self) -> None:
        class AToken(Token):
            pass

        class AAToken(Token):
            pass

        registry: TokenRegistry = TokenRegistry()
        registry.register(AToken, r"a")
        registry.register(AAToken, r"aa")

        match = registry.get_token("aaa")
        assert match is not None
        assert isinstance(match[0]("aa"), AAToken)


class VerifyGetTokenTestCase:
    def verify_get_token_no_text(self) -> None:
        lexer: Lexer = Lexer()
        register_parens(lexer)

        token_match = lexer.tokens.get_token("")
        assert token_match is None

    def verify_get_token_no_text_no_tokens(self) -> None:
        lexer: Lexer = Lexer()
        token_match = lexer.tokens.get_token("")
        assert token_match is None

    def verify_get_token_unmatched(self) -> None:
        lexer: Lexer = Lexer()
        register_parens(lexer)

        token_match = lexer.tokens.get_token("aaa")
        assert token_match is None

    def verify_get_token_no_tokens(self) -> None:
        lexer: Lexer = Lexer()
        register_parens(lexer)

        token_match = lexer.tokens.get_token("aaa")
        assert token_match is None

    def verify_get_token(self) -> None:
        lexer: Lexer = Lexer()
        register_parens(lexer)

        match = lexer.tokens.get_token("(((")
        assert match is not None
        token_factory_fn, re_match = match

        assert isinstance(token_factory_fn("("), LeftParen)
        assert re_match is not None

    def verify_get_token_picks_first(self) -> None:
        lexer: Lexer = Lexer()
        register_parens(lexer)

        token_match = lexer.tokens.get_token("aa(((")
        assert token_match is None

    def verify_get_token_scans_all_possible_tokens(self) -> None:
        lexer: Lexer = Lexer()
        register_parens(lexer)

        match = lexer.tokens.get_token(")(")
        assert match is not None
        token_factory_fn, re_match = match

        assert isinstance(token_factory_fn(")"), RightParen)
        assert re_match is not None

    def verify_longest_match(self) -> None:
        lexer: Lexer = Lexer()

        class AToken(Token):
            pass

        class AAToken(Token):
            pass

        lexer.register_token(AToken, r"a")
        lexer.register_token(AAToken, r"aa")

        match = lexer.tokens.get_token("aaa")
        assert match is not None

        token_factory_fn, re_match = match
        assert isinstance(token_factory_fn("aa"), AAToken)


class VerifyRegisterTokensTestCase:
    """Tests for Lexer.register_token / Lexer.register_tokens."""

    def verify_register_token(self) -> None:
        class AToken(Token):
            pass

        lexer: Lexer = Lexer()
        assert 0 == len(lexer.tokens)

        lexer.register_token(AToken, r"a")
        assert 1 == len(lexer.tokens)

    def verify_register_tokens(self) -> None:
        class AToken(Token):
            pass

        class BToken(Token):
            pass

        lexer: Lexer = Lexer()
        assert 0 == len(lexer.tokens)

        lexer.register_token(AToken, r"a")
        lexer.register_token(BToken, r"b")
        assert 2 == len(lexer.tokens)

        match_a = lexer.tokens.get_token("a")
        assert match_a is not None
        token_factory_fn_a, re_match_a = match_a

        assert isinstance(token_factory_fn_a("a"), AToken)
        assert re_match_a is not None

        match_b = lexer.tokens.get_token("b")
        assert match_b is not None
        token_factory_fn_b, re_match_b = match_b

        assert isinstance(token_factory_fn_b("b"), BToken)
        assert re_match_b is not None


class VerifyLexTestCase:
    def verify_lex_empty(self) -> None:
        lexer: Lexer = Lexer()
        tokens = lexer.lex("")
        assert 0 == len(tokens)

    def verify_lex_tokens(self) -> None:
        text = "((((((()()()))))))((((((("
        lexer: Lexer = Lexer()
        register_parens(lexer)

        tokens = lexer.lex(text)
        assert len(text) == len(tokens)
        for i, token in enumerate(tokens[:-1]):
            assert text[i] == token.text
            if token.text == "(":
                assert isinstance(token, LeftParen)
            else:
                assert isinstance(token, RightParen)

    def verify_lex_skips_blank(self) -> None:
        lexer: Lexer = Lexer()
        register_parens(lexer)

        tokens = lexer.lex("  (")
        assert 1 == len(tokens)
        assert "(" == tokens[0].text
        assert isinstance(tokens[0], LeftParen)

    def verify_lex_custom_blank_chars(self) -> None:
        lexer: Lexer = Lexer(blank_chars={"a", " "})
        register_parens(lexer)

        tokens = lexer.lex(" a(")
        assert 1 == len(tokens)
        assert "(" == tokens[0].text
        assert isinstance(tokens[0], LeftParen)

    def verify_lex_invalid_char(self) -> None:
        lexer: Lexer = Lexer()
        with pytest.raises(LexerException) as cm:
            lexer.lex("foo")
        assert cm.value.position == 0

    def verify_lex_error_position(self) -> None:
        class AToken(Token):
            pass

        lexer: Lexer = Lexer()
        lexer.register_token(AToken, r"a")

        with pytest.raises(LexerException) as cm:
            lexer.lex("aaaabaaa")
        assert cm.value.position == 4
