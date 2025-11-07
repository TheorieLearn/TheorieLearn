from queue import Queue
from typing import Iterable, Literal, TypedDict, cast

import prairielearn as pl
from theorielearn.automata_utils.fa_utils import generate_random_nfa
import theorielearn.shared_utils as su
from automata.fa.nfa import NFA, NFAStateT

StateQuestionNameT = Literal["e0_reach", "e1_reach", "transition_0", "transition_1"]
IsAcceptingTextT = Literal["yes", "no"]


class RowDict(TypedDict):
    "A class with type signatures for the question row dict"

    q: NFAStateT
    e0_reach: str
    e1_reach: str
    transition_0: str
    transition_1: str
    states_to_add: list[NFAStateT]
    is_accepting: IsAcceptingTextT
    is_upcoming: bool
    is_current: bool
    is_finished: bool


def sort_string(s: str | Iterable[str]) -> str:
    "Returns a string that is a sorted version of s with spaces removed"
    return ("".join(sorted(s))).replace(" ", "")


def convert_empty_set(s: str) -> str:
    return "∅" if not s else s


def grade_current_row(data: su.QuestionData) -> None:
    "Grade the currently active row"

    current_row_number: int = data["params"]["current_row_number"]
    current_row: RowDict = data["params"]["table_rows"][current_row_number]

    def get_question_name(question_name: str) -> str:
        return f"{current_row_number}-{question_name}"

    def grade_state_set_question(question_name: StateQuestionNameT) -> None:
        su.grade_question_parameterized(
            data,
            get_question_name(question_name),
            lambda x: (
                sort_string(x) == convert_empty_set(current_row[question_name]),
                None,
            ),
        )

    def grade_states_to_add(student_input: str) -> tuple[bool, str | None]:
        cleaned_student_input = set(map(sort_string, su.tokenize_string(student_input)))
        correct_answer = set(map(convert_empty_set, current_row["states_to_add"]))

        if cleaned_student_input == {""}:
            cleaned_student_input = set()

        return (cleaned_student_input == correct_answer, None)

    grade_state_set_question("e0_reach")
    grade_state_set_question("e1_reach")
    grade_state_set_question("transition_0")
    grade_state_set_question("transition_1")

    su.grade_question_parameterized(
        data,
        get_question_name("is_accepting"),
        lambda x: (x.lower().replace(" ", "") == current_row["is_accepting"], None),
    )

    su.grade_question_parameterized(
        data, get_question_name("states_to_add"), grade_states_to_add
    )

    pl.set_weighted_score_data(data)


def generate_table_list(question_nfa: NFA) -> list[RowDict]:
    "Generate a list corresponding to rows of the table for the NFA question"

    # Queue keeping states we have not filled in rows for
    state_queue: Queue[str] = Queue()
    states_in_table: set[str] = set()
    all_table_rows: list[RowDict] = []

    initial_state = question_nfa.initial_state
    closures = question_nfa._get_lambda_closures() #type: ignore
    initial_e_reach = sort_string(
        set().union(*(closures[i] for i in initial_state))
    )

    state_queue.put(initial_e_reach)
    states_in_table.add(initial_e_reach)

    while not state_queue.empty():
        state = state_queue.get()

        correct_0_transition = sort_string(
            set().union(*(question_nfa.transitions[i].get("0", set()) for i in state))
        )
        correct_1_transition = sort_string(
            set().union(*(question_nfa.transitions[i].get("1", set()) for i in state))
        )
        correct_e0_reach = sort_string(
            set().union(
                *(closures[i] for i in correct_0_transition)
            )
        )
        correct_e1_reach = sort_string(
            set().union(
                *(closures[i] for i in correct_1_transition)
            )
        )

        is_accepting: IsAcceptingTextT = (
            "no" if set(question_nfa.final_states).isdisjoint(state) else "yes"
        )

        states_to_add = sorted({correct_e0_reach, correct_e1_reach} - states_in_table)

        # Make sure that everything gets marked once it goes on the queue
        for next_state in states_to_add:
            states_in_table.add(next_state)
            state_queue.put(next_state)

        # Fill dictionary for current row
        all_table_rows.append(
            {
                "q": state,
                "e0_reach": correct_e0_reach,
                "e1_reach": correct_e1_reach,
                "transition_0": correct_0_transition,
                "transition_1": correct_1_transition,
                "states_to_add": states_to_add,
                "is_accepting": is_accepting,
                "is_upcoming": False,
                "is_current": False,
                "is_finished": False,
            }
        )

    return all_table_rows


def set_row_list_upcoming(row_list: list[RowDict], state_names: list[str]) -> None:
    "Set upcoming entries in row list"
    for row_dict in row_list:
        if row_dict["q"] in state_names:
            row_dict["is_upcoming"] = True


def set_row_list_current(row_list: list[RowDict], idx: int) -> None:
    "Set current entry in row list by idx"
    row_dict = row_list[idx]
    row_dict["is_current"] = True
    row_dict["is_upcoming"] = False


def set_row_finished(row_dict: RowDict) -> None:
    "Change row_dict to finished status. is_upcoming should already be false."
    row_dict["is_finished"] = True
    row_dict["is_current"] = False


def generate(data: su.QuestionData) -> None:
    # Generate initial NFA and row data
    question_nfa: NFA = cast(NFA, None)
    row_table_list = None

    while row_table_list is None or len(row_table_list) > 10 or len(row_table_list) < 8:
        question_nfa = generate_random_nfa(
            states=6, alphabet="01", edge_density=0.8, epsilon_density=0.2, accepting=2
        )
        row_table_list = generate_table_list(question_nfa)

    set_row_list_current(row_table_list, 0)

    # Set display for NFA and row data
    data["params"]["nfa_graph"] = question_nfa.show_diagram().string()
    data["params"]["table_rows"] = row_table_list

    # Set current row index
    data["params"]["current_row_number"] = 0


def grade(data: su.QuestionData) -> None:
    table_rows: list[RowDict] = data["params"]["table_rows"]
    current_row_number: int = data["params"]["current_row_number"]

    # Only do something if we haven't done the whole table yet
    if current_row_number < len(table_rows):
        # Grade current row
        grade_current_row(data)

        # Move on to custom grading
        if data["score"] == 1:
            current_row = table_rows[current_row_number]

            # Set current row to be finished, and set future states that will be visited
            set_row_finished(current_row)
            set_row_list_upcoming(table_rows, current_row["states_to_add"])

            current_row_number += 1
            data["params"]["current_row_number"] = current_row_number

            # If not finished, set next row to be current
            if current_row_number < len(table_rows):
                set_row_list_current(table_rows, current_row_number)

            # If finished, set done marker
            else:
                data["params"]["is_done"] = True

            # Use to set feedback for last submission correct
            data["params"]["last_submission_correct"] = True
        else:
            # Use to set feedback for last submission incorrect
            data["params"]["last_submission_correct"] = False

    data["score"] = current_row_number / len(table_rows)
