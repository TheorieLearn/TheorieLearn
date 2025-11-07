from typing import Callable, List, Optional, Set

from theorielearn.scaffolded_writing.cfg import ScaffoldedWritingCFG
from theorielearn.scaffolded_writing.student_submission import StudentSubmission


class GraphStudentSubmission(StudentSubmission):
    def __init__(self, token_list: List[str], cfg: ScaffoldedWritingCFG) -> None:
        super().__init__(token_list, cfg)


ConstraintT = Callable[[GraphStudentSubmission], Optional[str]]


def used_both_graphs(submission: GraphStudentSubmission) -> Optional[str]:
    if not submission.does_path_exist("STATEMENT_ABOUT_G"):
        return "You didn't mention the input graph."
    if not submission.does_path_exist("STATEMENT_ABOUT_G_PRIME"):
        return "You didn't mention the output graph."
    return None


def used_iff_structure(submission: GraphStudentSubmission) -> Optional[str]:
    if submission.does_path_exist("CONJUNCTION", "if and only if"):
        return None

    return "The two halves of the claim are connected with the wrong logical operator."


def correct_object(objects: Set[str], *, isGprime: bool = False) -> ConstraintT:
    graph, var = (
        ("STATEMENT_ABOUT_G_PRIME", "G'") if isGprime else ("STATEMENT_ABOUT_G", "G")
    )

    def constraint(submission: GraphStudentSubmission) -> Optional[str]:
        for obj in objects:
            if submission.does_path_exist(graph, "OBJECT", obj):
                return None

        return f"Does the structure you selected for {var} work for the original problem statement?"

    return constraint


def defined_starting_location(object: str, *, isGprime: bool = False) -> ConstraintT:
    graph, var = (
        ("STATEMENT_ABOUT_G_PRIME", "G'") if isGprime else ("STATEMENT_ABOUT_G", "G")
    )

    def constraint(submission: GraphStudentSubmission) -> Optional[str]:
        if submission.does_path_exist(graph, "OBJECT", "DESCRIPTION", "starting from"):
            return None

        return f"Where does our {object} start in {var}?"

    return constraint


def defined_simple_terminal_node(
    correct_node: str,
    *,
    isEnd: bool = False,
    isGprime: bool = False,
    feedback: str = "",
) -> ConstraintT:
    graph, var = (
        ("STATEMENT_ABOUT_G_PRIME", "G'") if isGprime else ("STATEMENT_ABOUT_G", "G")
    )
    terminal, node = ("END_NODE", "end") if isEnd else ("START_NODE", "start")

    def constraint(submission: GraphStudentSubmission) -> Optional[str]:
        if submission.does_path_exist(
            graph, "OBJECT", "DESCRIPTION", terminal, correct_node
        ):
            return None

        return f"This is not the correct {node} node for {var}. {feedback}"

    return constraint


def defined_general_terminal_node(
    *, isEnd: bool = False, isGprime: bool = False
) -> ConstraintT:
    graph, var = (
        ("STATEMENT_ABOUT_G_PRIME", "G'") if isGprime else ("STATEMENT_ABOUT_G", "G")
    )
    terminal, node = ("END_NODE", "end") if isEnd else ("START_NODE", "start")
    general = "T_GENERAL" if isEnd else "S_GENERAL"

    def constraint(submission: GraphStudentSubmission) -> Optional[str]:
        if not submission.does_path_exist(
            graph, "OBJECT", "DESCRIPTION", terminal, general
        ):
            return f"Have you considered all possible {node} nodes in {var}?"
        return None

    return constraint
