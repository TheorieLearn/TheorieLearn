import base64
import re
from typing import List, Optional, Tuple

from nltk.grammar import CFG, Nonterminal


def find_last_correct_line(submission_lines: List[str], grammar: CFG) -> int:
    """
    Finds last correct line in a preprocessed student submission.
    @param submission_lines list[str]
        lines in student submission
    @param grammar nltk.CFG object
        object representing grammar for the problem
    @return int
        returns index of last correct line if there is an error in derivation between two lines
        if student submission is correct, return -1
    """
    for current_line_index in range(len(submission_lines) - 1):
        current_line, next_line = (
            submission_lines[current_line_index],
            submission_lines[current_line_index + 1],
        )
        potential_next_lines = set()

        for char_index in range(len(current_line)):
            productions = grammar.productions(lhs=Nonterminal(current_line[char_index]))
            for production in productions:
                rhs = "".join(map(str, production.rhs()))
                potential_next_lines.add(
                    current_line[:char_index] + rhs + current_line[char_index + 1 :]
                )

        if next_line not in potential_next_lines:
            return current_line_index
    return -1


def check_submission(
    submission_lines: List[str], grammar: CFG, target: str
) -> Tuple[bool, Optional[str]]:
    """
    Identifies errors in preprocessed student submissions
    @param lines list[str]
        lines in student submission
    @param grammar nltk.CFG object
        object representing grammar for the problem
    @param target str
        string in grammar to derive
    @return tuple[bool, Optional[str]]
        The first element of the return tuple is a boolean indicating whether the answer was correct
        (True for correct, False for incorrect)
        The second element of the return tuple is an optional string
        that gives feedback on the issue with the submission.
        If the answer is correct, this element will be None.
    """
    if not submission_lines or submission_lines[0] != "S":
        return False, "Your submission should start with 'S'."
    elif submission_lines[-1] != target:
        return False, "Your submission should end with the final string."
    last_correct_line = find_last_correct_line(submission_lines, grammar)
    if last_correct_line == -1:
        return True, None
    return False, (
        f"Check that you can go from line {last_correct_line + 1} "
        f"to line {last_correct_line + 2}."
    )


def preprocess_submission(b64_submission_text: bytes) -> List[str]:
    """
    Decode submission text, remove whitespace, and filter out any empty lines.
    @param b64_submission_text bytes
        student submission, encoded in base 64
    @return list[str]
        list of lines in student submission, with whitespace removed in each line
        lines which only contain whitespace are removed entirely from the return list
    """
    submission_text = base64.b64decode(b64_submission_text).decode("utf-8")
    whitespace_pattern = re.compile(r"\s+")
    cleaned_lines = [
        re.sub(whitespace_pattern, "", line) for line in submission_text.split("\n")
    ]
    return [line for line in cleaned_lines if len(line) != 0]


def convert_production_rules_to_latex(production_rules: List[str]) -> str:
    """
    Converts a list of production rules into LaTex string
    @param production_rules
        list of production rules
    @return string
        string representation of a CFG to be displayed in LaTeX
    """

    def convert_individual_rule_to_latex(rule: str) -> str:
        rule = rule.replace("->", r"&\rightarrow")
        rule = rule.replace("|", r"\mid")
        rule = rule.replace("e", r" \varepsilon")
        return rule

    return r" \\ ".join(map(convert_individual_rule_to_latex, production_rules))


def convert_production_rules_to_nltk(production_rules: List[str]) -> str:
    """
    Converts a list of production rules into a string that can be parsed by a nltk.CFG object
    @param production_rules
        list of production rules
    @return string
        string representation of a CFG parseable by nltk
    """

    def convert_individual_rule_to_nltk(rule: str) -> str:
        rule = rule.replace("e", "")
        rule = re.sub(r"[0-9]", r" '\g<0>' ", rule)
        rule = re.sub(r"[A-Z]", r" \g<0> ", rule)
        rule = re.sub(r"\s+", " ", rule)
        rule = rule.strip()
        return rule

    return "\n".join(map(convert_individual_rule_to_nltk, production_rules))
