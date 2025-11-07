from typing import Any, Dict, Tuple

import chevron
import prairielearn as pl
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from theorielearn.regular_expressions.parser import compute_nfa_from_regex_lines
from theorielearn.regular_expressions.utils import convert_regex_to_latex
from theorielearn.shared_utils import grade_question_parameterized

INVALID_INPUT_FEEDBACK = "There was a parsing issue in your input. Make sure to only include valid symbols in the alphabet."
MISSING_STRING_FEEDBACK = "It looks like you may have missed some string(s)."
FALSE_POSITIVE_FEEDBACK = "Your input is accepted by the student's NFA, but it is not matched by the regular expression."
FALSE_NEGATIVE_FEEDBACK = "Your input is rejected by the student's NFA, but it is matched by the regular expression."
BOTH_ACCEPTING_FEEDBACK = "Your input is both accepted by the student's NFA and matched by the regular expression."
NEITHER_ACCEPTING_FEEDBACK = "Your input is neither accepted by the student's NFA nor is it matched by the regular expression."
VALID_FOR_OTHER_BOX_FEEDBACK = "This would be a valid example for the other input box."
CORRECT_ANSWER_FEEDBACK = "Great job!"


def get_feedback(nfa_accepts: bool, regex_accepts: bool) -> str:
    if regex_accepts and not nfa_accepts:
        return FALSE_NEGATIVE_FEEDBACK
    elif not regex_accepts and nfa_accepts:
        return FALSE_POSITIVE_FEEDBACK
    elif regex_accepts and nfa_accepts:
        return BOTH_ACCEPTING_FEEDBACK
    else:
        return NEITHER_ACCEPTING_FEEDBACK


def generate(data: Dict[str, Any]) -> None:
    regex = data["params"]["regex_string"]
    data["params"]["regex_latex"] = convert_regex_to_latex(regex)
    with open(
        data["options"]["server_files_course_path"] + "/theorielearn/thompson/question_base.html"
    ) as f:
        data["params"]["html"] = chevron.render(f, data).strip()


def grade(data: pl.QuestionData, nfa: NFA) -> None:
    nfa_equiv_dfa = DFA.from_nfa(nfa)

    def grade_counterexample(
        student_ans: str, regex_nfa: NFA, grading_false_neg: bool
    ) -> Tuple[bool, str]:
        regex_equiv_dfa = DFA.from_nfa(regex_nfa)

        answer_exists = (
            regex_equiv_dfa > nfa_equiv_dfa
            if grading_false_neg
            else regex_equiv_dfa < nfa_equiv_dfa
        )

        if student_ans.lower() == "none":
            if answer_exists:
                return False, MISSING_STRING_FEEDBACK
            else:
                return True, CORRECT_ANSWER_FEEDBACK

        if not student_ans or (
            student_ans != "e" and not all(char in {"0", "1"} for char in student_ans)
        ):
            return False, INVALID_INPUT_FEEDBACK

        student_ans = "" if student_ans == "e" else student_ans

        nfa_accepts = nfa.accepts_input(student_ans)
        regex_accepts = regex_nfa.accepts_input(student_ans)

        feedback = get_feedback(nfa_accepts, regex_accepts)

        is_false_neg = regex_accepts and not nfa_accepts
        is_false_pos = not regex_accepts and nfa_accepts

        if (
            is_false_neg
            and grading_false_neg
            or is_false_pos
            and (not grading_false_neg)
        ):
            return True, CORRECT_ANSWER_FEEDBACK

        if (
            is_false_neg
            and (not grading_false_neg)
            or is_false_pos
            and grading_false_neg
        ):
            return False, feedback + " " + VALID_FOR_OTHER_BOX_FEEDBACK

        return False, feedback

    regex_nfa = compute_nfa_from_regex_lines(data["params"]["regex_string"])

    grade_question_parameterized(
        data, "false_negative", lambda x: grade_counterexample(x, regex_nfa, True)
    )

    grade_question_parameterized(
        data, "false_positive", lambda x: grade_counterexample(x, regex_nfa, False)
    )

    pl.set_weighted_score_data(data)

    with open(
        data["options"]["server_files_course_path"] + "/theorielearn/thompson/submission_base.html"
    ) as f:
        data["feedback"]["submission_html"] = chevron.render(f, data).strip() #type: ignore
