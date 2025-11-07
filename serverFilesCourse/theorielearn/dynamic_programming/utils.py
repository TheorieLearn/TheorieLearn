import functools
import sys
from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

import numpy as np

from theorielearn.dynamic_programming.arbitrary_index_array import ElementT
from theorielearn.dynamic_programming.memo_array import MemoArray

NAN_ANSWER_FEEDBACK = "Your final answer references an uninitialized entry. Make sure to initialize any entries in the array before referencing them."


# A enum mapping correct answers to their respective text bodies.
class Answers(Enum):
    DECLARE_FUNC = "Declare Function"
    STATE_OUTPUT = "Clearly State Output"
    EXPLAIN_PARAMS = "Explain Parameters"
    COMPUTE_FINAL = "Can Compute Final Answer"
    REDUCES_RECURSIVE = "Reduces Recursively"
    VIABLE = "Viable  (all requirements satisfied)"


class StudentFeedback(NamedTuple):
    "A named tuple for the description of the differences for student feedback"

    feedback: List[str]
    grade: float


# This function can only be used in setup_code.py files.
# Calling disable_implicit_dp will disable implicit DP throughout the rest of the file.
def disable_implicit_dp():
    from code_feedback import Feedback

    # this import needs to be inside of the function
    # because code_feedback is only available in the Python external grader

    sys.setrecursionlimit = Feedback.not_allowed
    functools.lru_cache = Feedback.not_allowed
    functools.cache = Feedback.not_allowed
    functools.cached_property = Feedback.not_allowed


# This function generates the series of dropdowns to be added for english subproblem descriptions
def generate_english_subproblem(
    data: Dict[str, Any],
    problem_list: List[Tuple[str, Answers]],
    body_param: str,
    preamble_param: Optional[str],
    answer_names: Optional[list[str]] = None,
) -> None:
    preamble = """
<hr/>
<markdown>
Let's develop the dynamic programming algorithm according to how you learned in lecture! _[(See textbook)](https://courses.engr.illinois.edu/cs374/fa2021/A/notes/03-dynprog.pdf#page=10)_
When approaching a dynamic programming question, the _first and foremost_ task is to create an English definition
for your recursive subproblem. No matter how trivial the problem may seem, having a clean definition for the subproblem
is *imperative* to creating a convincingly correct algorithm.

We are asking you to consider some potential subproblem definitions and determine which ones are viable for solving this problem.
Keep in mind that a viable subproblem definition must satisfy all of the following requirements. (Each requirement below has been assigned a short label so that we can easily refer to it later on.)
</markdown>
<hr/>
<ul>
    <li><b>Declare Function</b>: The definition must declare a function with a descriptive name and parameters that can be memoized.</li>
    <li><b>Clearly State Output</b>: The definition must clearly state what quantity the function outputs.</li>
    <li><b>Explain Parameters</b>: The definition must explain how the function's input parameters affect the output of the function. Furthermore, all variables mentioned in the definition must either be defined in the original problem or declared as function parameters.</li>
    <li><b>Can Compute Final Answer</b>: We can compute the final answer requested by the original problem using these subproblems. (This can either involve a single subproblem function call that directly returns the final answer, or combining together multiple function calls to obtain the final answer.)</li>
    <li><b>Reduces Recursively</b>: Each subproblem can be reduced to smaller problems that are also handled by the subproblem definition. In other words, it must be possible to write a recursive formula for computing the function declared in the subproblem definition.</li>
</ul>
<hr/>
For each potential subproblem definition below, select the <i>first</i> requirement from this list that is violated, or select <b>Viable</b> if all of these requirements are satisfied.
<hr/>
"""

    # Wraps an answer statement in the correct html tags for dropdowns
    def wrap_answer(statement: Answers, correct: bool) -> str:
        if correct:
            return '<pl-answer correct = "true">' + statement.value + "</pl-answer>"
        else:
            return "<pl-answer>" + statement.value + "</pl-answer>"

    # Takes an element from a problem list and generates the dropdown hmtl problem
    def question_element(index: int, answers_names: Optional[list[str]] = None) -> str:
        definition, answer = problem_list[index]
        options = "".join(wrap_answer(x, x == answer) for x in Answers)

        if answers_names is not None and index >= len(answers_names):
            raise ValueError(
                "The length of answers_name is less than the number of input statement."
            )
        answers_name = f"q{index}" if answers_names is None else answers_names[index]

        return f"""
        <li>
        <b>Definition: </b>{definition}
        <br/>
        <b>First violated requirement: </b>
        <pl-multiple-choice answers-name="{answers_name}" order="fixed" display="dropdown" hide-letter-keys="true">
            {options}
            </pl-multiple-choice>
        </li>
        <br/>
        """

    if preamble_param is not None:
        data["params"][preamble_param] = preamble
    data["params"][body_param] = "".join(
        question_element(k, answer_names) for k in range(len(problem_list))
    )


def generate_student_feedback(
    inputs: Dict[str, Any],
    student_ans: ElementT,
    student_arr: MemoArray,
    correct_ans: ElementT,
    correct_arr: MemoArray,
    print_output: bool = True,
) -> StudentFeedback:
    """
    Evaluates a student's memoization array result against a given solution and gives appropriate feedback. To be used in guided DP feedback problems.

    :param inputs: The input parameters given to the student. Mainly used for printing
    :param student_ans: The student's final answer to the DP problem
    :param student_arr: The student's final memoization array to the DP problem
    :param correct_ans: The correct final answer to the DP problem
    :param correct_arr: The correct final memoization array to the DP problem
    :param print_output: True if input array is to printed to the user
    :param extra_params: Any extra params to print (if needed)


    :return: A dictionary containing whther the student earned credit for the problem and any
    feedback to be printed (in order)
    """
    feedback = []
    if type(student_ans) is not type(correct_ans):
        if np.isnan(student_ans):
            feedback.append(NAN_ANSWER_FEEDBACK)
        else:
            feedback.append(
                "Your code did not return the answer in the correct format.\nMake sure to return the final answer and not the entire array."
            )
        return StudentFeedback(feedback=feedback, grade=0.0)

    diff = student_arr.diff(correct_arr)
    name = correct_arr.name

    points_possible = 4
    points_earned = 0

    has_wrong_bounds = diff.same_bounds is False
    has_uninit_vals = len(diff.uninitialized) > 0
    has_wrong_vals = diff.first_wrong_val is not None
    if has_wrong_bounds or has_wrong_vals or has_uninit_vals:
        if print_output:
            feedback.append(format_feedback_inputs(inputs))

        if has_wrong_bounds:
            feedback.append(
                f"Your code initialized {name} to have bounds {name}{student_arr.bounds}, but according\nto our subproblem domain, our bounds should be {name}{correct_arr.bounds}.\n"
            )

        if has_uninit_vals:
            feedback.append(
                f"Your code failed to evaluate {name} for the following indices:\n\t{diff.uninitialized}\n"
            )

        # Extra none comparison for mypy
        if has_wrong_vals and diff.first_wrong_val is not None:
            idx_str = ", ".join(map(str, diff.first_wrong_val))
            feedback.append(
                f"Your code failed to compute {name} correctly. The first incorrect value in your\narray was {name}[{idx_str}] which you evaluated as {student_arr[diff.first_wrong_val]}, whereas the correct value\nshould be {correct_arr[diff.first_wrong_val]}."
            )
    else:
        if student_ans == correct_ans:
            points_earned += 1
        else:
            if print_output:
                feedback.append(format_feedback_inputs(inputs))
            feedback.append(
                f"Your memoization array appears to be correct, but you returned final answer {student_ans},\nwhereas the correct final answer is {correct_ans}."
            )

    points_earned += (
        np.array([has_wrong_bounds, has_uninit_vals, has_wrong_vals]) == False
    ).sum()
    return StudentFeedback(feedback=feedback, grade=points_earned / points_possible)


def format_feedback_inputs(inputs: Dict[str, Any]) -> str:
    """Converts inputs dictionary in DP feedback into a formatted string for printing"""
    return (
        "Given input:\n"
        + "\n".join(["\t" + i + " = " + str(v) for i, v in inputs.items()])
        + "\n"
    )
