from base64 import b64encode
from typing import List

import pytest
from theorielearn.cfg_drill.utils import check_submission, preprocess_submission
from nltk.grammar import CFG


class VerifyServerBase:
    def verify_preprocess_empty_input(self) -> None:
        assert preprocess_submission(b64encode(str.encode(""))) == []

    @pytest.mark.parametrize(
        "submission_text,expected",
        [("S", ["S"]), (" ", []), ("\t   \t", [])],
    )
    def verify_preprocess_single_line(
        self, submission_text: str, expected: List[str]
    ) -> None:
        assert preprocess_submission(b64encode(str.encode(submission_text))) == expected

    @pytest.mark.parametrize(
        "submission_text,expected",
        [
            ("S\n01S\n01", ["S", "01S", "01"]),
            ("S\t\t\t\n01S\n01", ["S", "01S", "01"]),
            ("\n\n\n\n\n\n\n\nS\t\t\t\n01S\n01\n\n\n\n", ["S", "01S", "01"]),
            ("\n\n\n\n\n\n\n\n\t\t\t   \n\n\n\n", []),
        ],
    )
    def verify_preprocess_multiple_lines(
        self, submission_text: str, expected: List[str]
    ) -> None:
        assert preprocess_submission(b64encode(str.encode(submission_text))) == expected

    @pytest.mark.parametrize(
        "submission_lines,grammar,target,result",
        [
            ([], CFG.fromstring("S -> '0' S '1' |"), "01", False),
            (["0S1", "01"], CFG.fromstring("S -> '0' S '1' |"), "01", False),
            (["S", "0S1"], CFG.fromstring("S -> '0' S '1' |"), "01", False),
            (
                ["S", "0S1", "00S11", "01"],
                CFG.fromstring("S -> '0' S '1' |"),
                "01",
                False,
            ),
            (["S", "0S1", "01"], CFG.fromstring("S -> '0' S '1' |"), "01", True),
            (["A", "B", "C", "D"], CFG.fromstring("S -> '0' S '1' |"), "01", False),
        ],
    )
    def verify_check_submission(
        self, submission_lines: List[str], grammar: CFG, target: str, result: bool
    ) -> None:
        assert check_submission(submission_lines, grammar, target)[0] == result
