from enum import Enum
from typing import List, Optional, Tuple

import chevron
import re
import prairielearn as pl
from theorielearn.shared_utils import QuestionData, grade_question_tokenized
from sympy import Function, latex, log, symbols, sympify
from sympy.core.expr import Expr


class SequenceType(Enum):
    INCREASING_ARITHMETIC = "increasing arithmetic sequence"
    INCREASING_GEOMETRIC = "increasing geometric sequence"
    DECREASING_ARITHMETIC = "decreasing arithmetic sequence"
    DECREASING_GEOMETRIC = "decreasing geometric sequence"
    CONSTANT = "constant sequence"


def generate(data: QuestionData, A: int, B: int, C: int, D: int, E: int) -> None:
    populate_data_dictionary_two_term_geometric(data, A, B, C, D, E)

    incorr_patterns = [
        SequenceType.INCREASING_ARITHMETIC.value,
        SequenceType.DECREASING_ARITHMETIC.value,
        SequenceType.INCREASING_GEOMETRIC.value,
        SequenceType.DECREASING_GEOMETRIC.value,
        SequenceType.CONSTANT.value,
    ]

    incorr_bigo = [
        "dominated by the leaves of the tree",
        "dominated by the root",
        "work per level * number of levels",
    ]
    series_type = data["params"]["series_type"]
    incr = False
    decr = False
    # Constant
    if series_type == SequenceType.CONSTANT.value:
        corr_bigo = "work per level * number of levels"
    # Decreasing
    elif series_type == SequenceType.DECREASING_GEOMETRIC.value:
        corr_bigo = "dominated by the root"
        decr = True
    # Increasing
    else:
        corr_bigo = "dominated by the leaves of the tree"
        incr = True

    incorr_bigo.remove(corr_bigo)
    incorr_patterns.remove(series_type)

    data["params"]["corr_pattern"] = [series_type]
    data["params"]["incorr_pattern"] = incorr_patterns

    data["params"]["corr_bigo"] = [corr_bigo]
    data["params"]["incorr_bigo"] = incorr_bigo

    data["params"]["numlvls"] = not decr
    data["params"]["leaves"] = incr

    with open(
        data["options"]["server_files_course_path"]
        + "/theorielearn/recursion_tree/question_base.html"
    ) as f:
        data["params"]["html"] = chevron.render(f, data["params"]).strip()


def populate_data_dictionary_two_term_geometric(
    data: QuestionData, A: int, B: int, C: int, D: int, E: int
) -> None:
    """
    Populates the data dictionary for a recurrence of the form
    T(n) = A*T(n/B) + C*T(n/D) + O(n^E)

    Requires that B is greater than D (otherwise change order of terms)

    Supports recurrences with only one recursive term -- just set C = 0

    C must be 0 if it is an increasing geometric series
    """
    if B <= D:
        raise ValueError("B must be strictly greater than D.")
    T = Function("T")
    # comment explain
    n, l = symbols("n l")
    data["params"]["recursive_terms"] = latex(A * T(n / B) + C * T(n / D))
    data["params"]["big_O_term"] = latex(n**E)
    W0 = n**E
    W1 = A * (n / B) ** E + C * (n / D) ** E
    r = W1 / W0
    W2 = r**2 * W0
    Wl = r**l * W0
    if r > 1 and C != 0:
        raise ValueError("The value C must be 0 for increasing geometric sequences.")

    if r < 1:
        data["params"]["series_type"] = SequenceType.DECREASING_GEOMETRIC.value
    elif r == 1:
        data["params"]["series_type"] = SequenceType.CONSTANT.value
    else:
        data["params"]["series_type"] = SequenceType.INCREASING_GEOMETRIC.value

    data["correct_answers"]["level0-work-per-node"] = stringify([(n**E, 1)])
    data["correct_answers"]["level1-work-per-node"] = stringify(
        [((n / B) ** E, A), ((n / D) ** E, C)]
    )
    data["correct_answers"]["level2-work-per-node"] = stringify(
        [
            ((n / B**2) ** E, A**2),
            ((n / (B * D)) ** E, 2 * A * C),
            ((n / D**2) ** E, C**2),
        ]
    )
    data["correct_answers"]["level0-work-level"] = pl.to_json(W0)
    data["correct_answers"]["level1-work-level"] = pl.to_json(W1)
    data["correct_answers"]["level2-work-level"] = pl.to_json(W2)
    data["correct_answers"]["levell"] = pl.to_json(Wl)

    # Calculate depth of tree
    # Choose longest path to root
    depth_of_tree = log(n, B) if C == 0 else log(n, D)
    data["correct_answers"]["depth_of_tree"] = pl.to_json(depth_of_tree)
    data["correct_answers"]["work_at_leaves_exponent"] = pl.to_json(log(A, B))

    # Final Big O
    # Increasing --> This gives a weird error message on very specific incorrect inputs
    # (such as log(6,2), log(5/3,3), 1 + log(7) / log(2), n*log(6,2))
    # when the increasing case is inside the if statement.
    # not sure why, but moving it out here prevents the bug
    symp_A = sympify(A)
    symp_B = sympify(B)
    log_exp = log(symp_A, symp_B)
    full_exp = n**log_exp
    data["correct_answers"]["final_ans"] = str(full_exp)

    # Constant
    if data["params"]["series_type"] == SequenceType.CONSTANT.value:
        data["correct_answers"]["final_ans"] = str(log(n) * W0)
    # Decreasing
    elif data["params"]["series_type"] == SequenceType.DECREASING_GEOMETRIC.value:
        data["correct_answers"]["final_ans"] = str(W0)


def stringify(nodes: List[Tuple[Expr, int]]) -> str:
    """
    Takes in list of sympy expressions and format it to match student input format for grading.
    """

    return ",".join(
        str(new_node).replace("**", "^") for new_node in nodes if new_node[1] > 0
    )

def check_bad_input(submission: str) -> Optional[str]:
    if not isinstance(submission, str):
        submission = str(submission)

    if len(re.findall(r'\blog\b', submission)) > 2:
        return "Sanity Check: Too many instances of 'log'."

    # Check for exponents containing variables (checks ^ and **)
    exponent_pattern = re.compile(r'(\^|\*\*)\s*[\{\(\[]?\s*\d*[a-zA-Z]+\s*[\}\)\]]?')
    if exponent_pattern.search(submission):
        return "Sanity Check: Variables in exponents are not required."

def sanity_check(data: QuestionData) -> None:
    for question, answer in data["submitted_answers"].items():
        bad = check_bad_input(answer)
        if(bad):
            data["format_errors"][question] = bad

def grade(data: QuestionData) -> None:
    sanity_check(data)

    two_term_geometric_tokenized = [
        "level0-work-per-node",
        "level1-work-per-node",
        "level2-work-per-node",
    ]

    for question_name in two_term_geometric_tokenized:
        grade_question_tokenized(data, question_name)

    pl.set_weighted_score_data(data)
