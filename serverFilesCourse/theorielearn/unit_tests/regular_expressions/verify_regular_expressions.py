from typing import Union

import pytest
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from theorielearn.automata_utils.fa_utils import get_equiv_dfa
from pytest_lazyfixture import lazy_fixture
from theorielearn.regular_expressions.exceptions import RegexException
from theorielearn.regular_expressions.parser import compute_nfa_from_regex_lines
from theorielearn.shared_utils import strings_of_length_at_most_n

TEST_ALPHABET = {"0", "1"}
STRING_LENGTH_LIMIT = 7


@pytest.mark.parametrize(
    "re_string",
    [
        "01+",
        "+10",
        "11 (+001)",
        "(110+)  01",
        "(  + 01)",
        "(10  + )(*01)",
        "0+ *",
        "(0) + +",
        "(((01))",
        "((01)))",
        "0var0",
        "0=0",
        "var000",
        "*01",
        ")(",
        "1()0",
        "",
        " ",
        "     ",
    ],
)
def verify_exception_invalid_regex(re_string: str) -> None:
    "Checks that compute_nfa_from_regex_lines throws exception on invalid strings"
    with pytest.raises(RegexException):
        compute_nfa_from_regex_lines(re_string, TEST_ALPHABET)


@pytest.mark.parametrize(
    "re_string",
    [
        "(e+1)(01)*(e+0)",
        "(0+1)*010(0+1)*",
        "1*(01*01*)*",
        "0+1(0+1)*00",
        "((e+0+00+000)1)*(e+0+00+000)",
        "(0+1)(0+1)(0+1)(0+1)*",
        "((0+1)(0+1))*",
        "(1*0)*(0*1)*",
        "(00000)*",
        "0(0+1(1+0(0+11*)*)*)*",
    ],
)
def verify_parses_valid_regex(re_string: str) -> None:
    "Checks that compute_nfa_from_regex_lines doesn't throw an exception on valid strings"
    compute_nfa_from_regex_lines(re_string, TEST_ALPHABET)


def verify_compute_nfa_contains_000() -> None:
    "Tests with a regex checking that the target string contains 000"
    regex = "all = (0+1)* \n all 000 all"

    nfa = compute_nfa_from_regex_lines(regex, TEST_ALPHABET)

    for bitstring in strings_of_length_at_most_n(
        0, STRING_LENGTH_LIMIT, alphabet=TEST_ALPHABET
    ):
        if "000" in bitstring:
            assert nfa.accepts_input(bitstring)
        else:
            assert not nfa.accepts_input(bitstring)


def verify_compute_nfa_no_000() -> None:
    "Tests with a regex checking that the target string contains no 000"
    regex = "(e + 0 + 00)(1(e + 0 + 00))*"

    nfa = compute_nfa_from_regex_lines(regex, TEST_ALPHABET)

    for bitstring in strings_of_length_at_most_n(
        0, STRING_LENGTH_LIMIT, alphabet=TEST_ALPHABET
    ):
        if "000" not in bitstring:
            assert nfa.accepts_input(bitstring)
        else:
            assert not nfa.accepts_input(bitstring)


def verify_compute_nfa_runs_0_runs_at_least_3() -> None:
    """
    Tests with a regex checking that all runs of 0's in the target string
    have length at least 3
    """
    regex = "(e + 1) ((e + 0000*)1)* (e + 0000*)"

    nfa = compute_nfa_from_regex_lines(regex, TEST_ALPHABET)
    assert nfa.accepts_input("000")
    assert nfa.accepts_input("1111")
    assert nfa.accepts_input("000100001000")
    assert not nfa.accepts_input("001000")
    assert not nfa.accepts_input("001001")
    assert not nfa.accepts_input("00")


def verify_compute_nfa_at_least_3_0() -> None:
    """
    Tests with a regex checking all strings that have at least 3 zeros
    """
    regex = "all = (1 + 0)* \n all 0 all 0 all 0 all"

    nfa = compute_nfa_from_regex_lines(regex, TEST_ALPHABET)

    for bitstring in strings_of_length_at_most_n(
        0, STRING_LENGTH_LIMIT, alphabet=TEST_ALPHABET
    ):
        if sum(int(bit == "0") for bit in bitstring) >= 3:
            assert nfa.accepts_input(bitstring)
        else:
            assert not nfa.accepts_input(bitstring)


def verify_compute_nfa_at_least_two_0_at_least_one_1() -> None:
    """
    Tests with a regex checking all strings that have at least two 0s and one 1
    """
    regex = """
        all = (1 + 0)*
        first = 000* 1
        second =    011*0
        third = 11*01*0

        (first + second + third ) all
    """

    def at_least_two_0_at_least_one_1(bitstring):
        return (
            sum(int(bit == "0") for bit in bitstring) >= 2
            and sum(int(bit == "1") for bit in bitstring) >= 1
        )

    nfa = compute_nfa_from_regex_lines(regex, TEST_ALPHABET)

    for bitstring in strings_of_length_at_most_n(
        0, STRING_LENGTH_LIMIT, alphabet=TEST_ALPHABET
    ):
        if at_least_two_0_at_least_one_1(bitstring):
            assert nfa.accepts_input(bitstring)
        else:
            assert not nfa.accepts_input(bitstring)


@pytest.mark.parametrize(
    "regex_1, regex_2",
    [
        ("a = (0+1) \n a.a.a.a*", "(0+1)(0+1)(0+1)(0+1)*"),
        (
            "(00)*(11)*+0(00)*1(11)*+(00)*1(11)*0+0(00)*(11)*0",
            "A = (00)* \n B = (11)* \n (A B+0 A 1 B)+(0 A B +A1B)0",
        ),
        (
            "((00)*1(11)*+0(00)*(11)*)0+((00)*(11)*+0(00)*1(11)*)",
            "(00)*(e+01)(11)*+(0(00)*(e+(11)*)+(e+(00)*)1(11)*)0",
        ),
        (
            "(0(00)*(11)*+(00)*1(11)*)0+((00)*(11)*+0(00)*1(11)*)",
            "A = (00)* \n B = (11)* \n A B+(A)(1B)0+(0A)(B)0+(0A)(1B)",
        ),
        (
            "(00)*(11)*+(00)*(01)(11)*+(00)*(0+1)(11)*0",
            "AB = (00)* \n B = (11)* \n (AB B)+(0AB1B)+(0AB.B0)+(AB1B0)",
        ),
        (
            "(00)*(11)*+(00)*(1)(11)*0+0(00)*(11)*0+(0(00)*)(1(11)*)",
            "((00)*+(11)*+(00)*(01)(11)*+(00)*(11)*)+((00)*1(11)*+0(00)*(11)*)0",
        ),
        (
            "e+(00)*(00+01(11)*+11(11)*)+((00)*1(11)*+0(00)*(11)*)0",
            "((00)*(11)*+(00)*0(11)*1)+((00)*(11)*10+(00)*0(11)*0)",
        ),
        (
            "(0(00)*1(11)*)+((00)*(11)*)+(00)*1(11)*0+0(00)*(11)*0",
            "(00)*(11)*+0(00)*1(11)*+0(00)*(11)*0+(00)*1(11)*0",
        ),
        (
            "(00)*(11)*+(0)(00)*(11)*(0)+(00)*(1)(11)*(0)+(0)(00)*(1)(11)*",
            "(00)*(11)*+(00)*(0)(11)*(0)+(00)*(11)*(1)(0)+(00)*(0)(11)*(1)",
        ),
        (
            "(00)*01(11)*+(00)*0(11)*0+(00)*1(11)*0+(00)*(11)*",
            "0(00)*1(11)*+(00)*(11)*+0(00)*(11)*0+(00)*1(11)*0",
        ),
        (
            "(00)*(11)*+0(00)*(11)*0+(00)*1(11)*0+0(00)*1(11)*",
            "A = (00)* \n B = (11)* \n A.B+A0B0+A.B10+A0B1",
        ),
        (
            "((00)*(11)*+0(00)*1(11)*)+(0(00)*(11)*0+(00)*1(11)*0)",
            "0(00)*1(11)*+0(00)*(11)*0+(00)*1(11)*0+(00)*(11)*",
        ),
        (
            "(00)*((0+1)(11)*0+(e+01)(11)*)",
            "e+1(11)*0+0(00)*(0)+(00)*+(11)*+0(00)*1(11)*+(00)*(11)*+(00)*1(11)*0+0(00)*1+0(00)*(11)*0",
        ),
        (
            "(00)*(((11)*(e+10))+(0(11)*(1+0)))",
            "(00)*(11)*+0(00)*(11)*0+(00)*(11)*10+0(00)*(11)*1",
        ),
        (
            "(00)*(11)*+0(00)*(11)*0+0(00)*1(11)*+(00)*1(11)*0",
            "((00)*1(11)*0)+((00)*(11)*)+(0(00)*1(11)*)+(0(00)*(11)*0)",
        ),
        (
            "((00)*(11)*)+(0(00)*(11)*0)+((00)*1(11)*0)+(0(00)*1(11)*)",
            "(00)*(11)*+(00)*(11)*(1)(0)+(00)*(0)(11)*(0)+(00)*(0)(11)*(1)",
        ),
        (
            "(00)*0(11)*1+(00)*(11)*+(00)*(11)*10+(00)*0(11)*0",
            "(00)*(11)*+(00)*0(11)*1+(00)*0(11)*0+(00)*(11)*10",
        ),
        (
            "0(00)*1(11)*+(00)*(11)*+(00)*1(11)*0+0(00)*(11)*0",
            "((00)*(11)*)+((00)*1(11)*0)+(0(00)*(11)*0)+(0(00)*1(11)*)",
        ),
        (
            "(00)*0(11)*0+(00)*(11)*10+(00)*(11)*+(00)*0(11)*1",
            "0(00)*(11)*0+(00)*1(11)*0+(00)*(11)*+0(00)*1(11)*",
        ),
        (
            "(0(00)*1(11)*)+((00)*(11)*)+(0(00)*(11)*0)+((00)*1(11)*0)+e",
            "e+(00)*(1(11)*+0(11)*)(0+1)",
        ),
        ("((e + 1 + 11)0)*(e + 1 + 11)", "(0 + 10 + 110)*(e + 1 + 11)"),
        ("(e+1+11)(0(e+1+11))*", "(e + 1 + 11)(0 + 01 + 011)*"),
        ("((e+1+11)00*)*(e+1+11)", "(10+ 1 1 0 +0)*(1+11+e)"),
        ("(0+10+110)*(1+11+e)", "(0+110+10)*(e+1+11)"),
        ("(e + 1 + 11)(0(e + 1 + 11))*", "((e + 1 + 11)00*)*(e + 1 + 11)"),
        ("(0+10+110)*(e+1+11)", "(e+1+11)(00*(e+1+11))*"),
        ("(1+(00))*", "((00)*(1)*(00)*)*+((1)*(00)*)*"),
        ("(1*(00)*)*", "(1 + 00)*"),
        ("(e+11*)((00)*(11*))*(e+(00)*)", "((00)*1*(00)*)*"),
        ("((00) + 1)*", "((00)* + 1*)*"),
        ("(1*)((00)*1*)*(00)*", "((1)*(00)*(1)*)*"),
        ("((00)*+1)*", "(1+00)*1*(00+1)*"),
        ("(1 + e)*(e+00(00)*+1)*", "((00)*+1*)*"),
        ("(00 + 1)*", "(1 + (00)*)*"),
        ("(1*(00)*1*)*", "(1+00)*"),
        (
            "(1 + 01 + 001)*(e + 0 + 00) ",
            "A = (1 + 01 + 001)* \n B = A0(1A0 + 01A0)* \n C = B0(1B0)* \n A + B + C",
        ),
        ("(e+0+00)(1(e+0+00))*", "(01 + 001 + 1)*(e+0+00)"),
        ("((e+0+00)11*)*(0+00+e)", "(e + 0 + 00)(1( e + 0 + 00))*"),
        ("(1 + 01 + 001)*(e+ 0 + 00)", "(e+0+00)(1+100+10)*"),
        ("((e+0+00)1)*(e+0+00)", "(1+01+001)* (e+0 +00)"),
        (
            "(((001)*+(01)*+1*)*0)+(((001)*+(01)*+1*)*00) + ((001)*+(01)*+1*)*",
            "(1 + 10 + 100)* + (1 + 01 + 001)* + 0(1 + 10 + 100)* + (1 + 01 + 001)*0 + 00(1 + 10 + 100)* + (1 + 01 + 001)*00",
        ),
        ("(1+01+001)*(0+00+e)", "1*(1 + 01 + 001)* (e + 0 + 00)"),
        ("(1+01+001)*(0+00)+(1+01+001)*", "(e+11*)((0+00)(11*))*(e+0+00)"),
        ("(1+01*01*0)*01*01*", "A=(1*01*01*0 + 1*)* \n A0A0A"),
        ("(01*01*01*)*1*01*01*(01*01*01*)*", "((1*01*)(1*01*)(1*01*))*(1*01*)(1*01*)"),
        ("(1+01*01*0)*(01*01*)", "1*01*01*(1*01*01*01*)*"),
        ("(1*01*01*01*)*(1*01*01*)", "1*01*01*(e+ 01*01*01*)*"),
        ("(1*01*01*)(01*01*01*)*", "(1*01*01*)(1*01*01*01*)*"),
        (
            "(1*01*01*01*+1*)*01*01* + 1*0(1*01*01*01*+1*)*01* + 1*01*0(1*01*01*01*+1*)*",
            "1*01*01*(01*01*01*)*",
        ),
        (
            "all = (0*1*)* \n all1all0all0all+all0all1all0all+all0all0all1all",
            "((0 +1)*1(0+1)*0(0+1)*0(0+1)*) + ((0 +1)*0(0+1)*1(0+1)*0(0+1)*) + ((0 +1)*0(0+1)*0(0+1)*1(0+1)*)",
        ),
        (
            "(0+1)*0(0+1)*0(0+1)*1(0+1)* + (0+1)*0(0+1)*1(0+1)*0(0+1)* + (0+1)*1(0+1)*0(0+1)*0(0+1)*",
            "000*1(0+1)* + 00*11*0(0+1)* + 11*01*0(0+1)*",
        ),
        (
            "(0+1)*1(0+1)*0(0+1)*0+(0+1)*0(0+1)*0(0+1)*1(0+1)*+(0+1)*0(0+1)*1(0+1)*0(0+1)*",
            "(0+1)*0(0+1)*0(0+1)*1(0+1)*+(0+1)*0(0+1)*1(0+1)*0(0+1)*+ (0+1)*1(0+1)*0(0+1)*0(0+1)*",
        ),
        (
            "000*1(0+1)* + 011*0(0+1)* + 11*01*0(0+1)*",
            "(0+1)*0(0+1)*1(0+1)*0(0+1)* + (0+1)*1(0+1)*0(0+1)*0(0+1)* + (0+1)*0(0+1)*0(0+1)*1(0+1)*",
        ),
        (
            "(0 + 1)*0(0 + 1)*0(0 + 1)*1(0 + 1)* +  (0 + 1)*0(0 + 1)*1(0 + 1)*0(0 + 1)* +  (0 + 1)*1(0 + 1)*0(0 + 1)*0(0 + 1)*",
            "A=(0 + 1)* \n A0A0A1A + A0A1A0A + A1A0A0A",
        ),
        (
            "(1+0)*11*000*(1+0)* + (1+0)*00*11*00*(1+0)* + (1+0)*000*11*(1+0)*",
            "(0+1)*0((0+1)*10(0+1)*+(0+1)*01(0+1)*)+((0+1)*10(0+1)*+(0+1)*01(0+1)*)0(0+1)*",
        ),
        (
            "(1+e)0(1+0)*0(1+0)*1(1+0)*+(1+e)0(1+0)*1(1+0)*0(1+0)*+(0+e)1(1+0)*0(1+0)*0(1+0)*",
            "R=(0+1)* \n (R)(1R0R0+0R1R0+0R0R1)(R)",
        ),
        (
            "(0+1)*001(0+1)* + (0+1)*011*0(0+1)* + (0+1)*100(0+1)*",
            "(0+1)*0(0+1)*0(0+1)*1+(0+1)*1(0+1)*0(0+1)*0+(0+1)*0(0+1)*1(0+1)*0",
        ),
        (
            "(0+1)*(100+01(1*)0+001)(0+1)*",
            "(0+1)*1(0+1)*0(0+1)*0(0+1)* + (0+1)*0(0+1)*1(0+1)*0(0+1)* + (0+1)*0(0+1)*0(0+1)*1(0+1)*",
        ),
        (
            "(11*01*0(0+1)*)+(1*011*0(0+1)*)+(0*1*01*01(0+1)*)",
            "(0+1)*(0)(0+1)*(0)(0+1)*(1)(0+1)*+(0+1)*(0)(0+1)*(1)(0+1)*(0)(0+1)*+(0+1)*(1)(0+1)*(0)(0+1)*(0)(0+1)*",
        ),
        (
            "00(0)*1(0+1)* + 01(1)*0(0+1)* + 1(1)*01*0(0+1)*",
            "(1+0)* (0(1+0)*0(1+0)*1 + 0(1+0)*1(1+0)*0 + 1(1+0)*0(1+0)*0) (1 + 0)*",
        ),
        (
            "(0+1)*0(0 + 1)*1(0 + 1)*0(0 + 1)* + (0+1)*0(0 + 1)*0(0 + 1)*1(0 + 1)* + (0+1)*1(0 + 1)*0(0 + 1)*0(0 + 1)*",
            "(0+1)*(001)(0+1)*+(0+1)*(011*0)(0+1)*+(0+1)*(100)(0+1)*",
        ),
        (
            "1(0+1)*0(0+1)*0(0+1)* + 0(0+1)*0(0+1)*1(0+1)* + 0(0+1)*1(0+1)*0(0+1)*",
            "((0 + 1)*0(0 + 1)*0(0 + 1)*1(0 + 1)*) + ((0 + 1)*0(0 + 1)*1(0 + 1)*0(0 + 1)*) + ((0 + 1)*1(0 + 1)*0(0 + 1)*0(0 + 1)*) ",
        ),
        ("(0*1*)*(001 + 011*0 + 100)(0*1*)*", "(000*1 + 011*0 + 11*01*0)(0+1)*"),
        (
            "(0+1)*1(0+1)*0(0+1)*0(0+1)* + (0+1)*0(0+1)*1(0+1)*0(0+1)*+ (0+1)*0(0+1)*0(0+1)*1(0+1)*",
            "(0 +1)*0(0+1)*0(0+1)*1(0+1)* + (0 +1)*0(0+1)*1(0+1)*0(0+1)*  + (0 +1)*1(0+1)*0(0+1)*0(0+1)* ",
        ),
        ("(000*1 + 011*0 + 11*01*0)(0 + 1)*", "A=(1+0)* \n 1A0A0A+0A1A0A+0A0A1A"),
        (
            "(0 + 1)*0(0 + 1)*0(0 + 1)*1(0 + 1)* + (0 + 1)*1(0 + 1)*0(0 + 1)*0(0 + 1)* + (0 + 1)*0(0 + 1)*1(0 + 1)*0(0 + 1)*",
            "((0+1)* 0 (0+1)* 0 (0+1)* 1 (0+1)*) + ((0+1)* 1 (0+1)* 0 (0+1)* 0 (0+1)*) + ((0+1)* 0 (0+1)* 1 (0+1)* 0 (0+1)*)",
        ),
        (
            "((0+1)*0(0+1)*0(0+1)*1(0+1)*)+((0+1)*0(0+1)*1(0+1)*0(0+1)*)+((0+1)*1(0+1)*0(0+1)*0(0+1)*)",
            "(000*1+(11*01*0)+(00*11*00*))(0+1)*",
        ),
        (
            "(0*1*)*(11*00 + 011*0 + 0011*)(0*1*)*",
            "(0+1)*001(0+1)* + (0+1)*01*10(0+1)* + (0+1)*100(0+1)*",
        ),
        (
            "(0+1)*(1001(0+1)*1001 + 1001001)(0+1)*",
            "(0+1)*1001(0+1)*1001(0+1)*+(0+1)*1001001(0+1)*",
        ),
        (
            "(0+1)*1001(e+(0+1)*1)001(0+1)*",
            "(1 + 0)*1001001(1 + 0)* + (1 + 0)*1001(1+0)*1001(1 + 0)*",
        ),
        (
            "(1+0)*100 1001(1+0)*+(1+0)*1001(1+0)*1001(1+0)*",
            "(0+1)*10 01(0+1)*10 01(0+1)* + (0+1)*1001 001(0+1)*",
        ),
    ],
)
def verify_regex_equiv(regex_1: str, regex_2: str) -> None:
    input_symbols = {"0", "1"}
    dfa_1 = DFA.from_nfa(compute_nfa_from_regex_lines(regex_1, input_symbols))
    dfa_2 = DFA.from_nfa(compute_nfa_from_regex_lines(regex_2, input_symbols))
    assert dfa_1 == dfa_2


@pytest.mark.parametrize(
    "reference_fa, target_regex",
    [
        (lazy_fixture("regex_1_nfa"), "(01 + 1)*(0*1 + 1*0)(10 + 0)*"),
        (lazy_fixture("regex_2_nfa"), "(1(010)*(11)* + 010)*"),
        (lazy_fixture("regex_3_dfa"), "0(0 + 1)*0 + 1(0 + 1)*1"),
        (lazy_fixture("regex_4_dfa"), "(0 + 1)*00 + (0 + 1)*11"),
        (lazy_fixture("regex_5_nfa"), "(((01)*0 + 2)(100)*1)*(1* + 0*2*)"),
        (lazy_fixture("at_least_three_1_dfa"), "A = (1 + 0)* \n A 1 A 1 A 1 A"),
        (lazy_fixture("accepts_everything_dfa"), "(1*0)*(0*1)*"),
        (lazy_fixture("words_ending_in_1_dfa"), "A = (1 + 0)* \n A1"),
    ],
)
def verify_regex_parsing(reference_fa: Union[DFA, NFA], target_regex: str) -> None:
    parsed_equiv_dfa = DFA.from_nfa(
        compute_nfa_from_regex_lines(target_regex, set(reference_fa.input_symbols))
    )
    equiv_reference_dfa = get_equiv_dfa(reference_fa)
    assert parsed_equiv_dfa == equiv_reference_dfa
