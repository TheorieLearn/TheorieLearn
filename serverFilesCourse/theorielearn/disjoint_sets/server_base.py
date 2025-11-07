import random
from typing import Optional, TypedDict

import chevron
import theorielearn.shared_utils as su
from theorielearn.shared_utils import QuestionData


class RowDict(TypedDict):
    "A class with type signatures for the question row dict"

    union: tuple[int, int]
    union_display: str
    set_state: list[int]
    set_state_display: str
    is_upcoming: bool
    is_current: bool
    is_finished: bool
    attempts: int


def set_row_list_current(row_list: list[RowDict], idx: int) -> None:
    "Set current entry in row list by idx"
    row_dict = row_list[idx]
    row_dict["is_current"] = True
    row_dict["is_upcoming"] = False


def generate_table_list(
    states: list[list[int]], unions: list[tuple[int, int]]
) -> list[RowDict]:
    "Generate a list corresponding to rows of the table for the NFA question"
    union_displays = display_unions(unions)
    all_table_rows: list[RowDict] = [
        {
            "union": union,
            "union_display": union_display,
            "set_state": state,
            "set_state_display": display_list(state),
            "is_upcoming": False,
            "is_current": False,
            "is_finished": False,
            "attempts": 0,
        }
        for state, union, union_display in zip(states, unions, union_displays)
    ]
    return all_table_rows


class DisjointSetUnion:
    __slots__ = ("num_sets", "parent", "pc")
    num_sets: int
    parent: list[int]
    pc: bool

    def __init__(self, n: int, pc: bool, init_sets: Optional[list[int]] = None) -> None:
        if init_sets is not None:
            self.parent = init_sets.copy()
        else:
            self.parent = [-1 for _ in range(n)]

        self.num_sets = n
        self.pc = pc

    def __find_no_pc(self, x: int) -> int:
        if self.parent[x] < 0:
            return x
        return self.__find(self.parent[x])

    def __find(self, x: int) -> int:
        if self.parent[x] < 0:
            return x
        self.parent[x] = self.__find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        if self.pc:
            self.__union_pc(a, b)
        else:
            self.__union_no_pc(a, b)

    def __union_pc(self, a: int, b: int) -> None:
        a = self.__find(a)
        b = self.__find(b)
        if a == b:
            return
        if self.parent[a] > self.parent[b]:  # negative numbers
            a, b = b, a
        self.num_sets -= 1
        self.parent[a] += self.parent[b]  # there both roots
        self.parent[b] = a

    def __union_no_pc(self, a: int, b: int) -> None:
        a = self.__find_no_pc(a)
        b = self.__find_no_pc(b)
        if a == b:
            return
        if self.parent[a] > self.parent[b]:  # negative numbers
            a, b = b, a
        self.num_sets -= 1
        self.parent[a] += self.parent[b]  # there both roots
        self.parent[b] = a

    def get_parent(self) -> list[int]:
        return self.parent


# generates a random list of unions -> each union will change the list representation of our set.
def random_unions_diff_sets_with_answers(
    n: int, disjoint_set: DisjointSetUnion, num_sets: int = 10
) -> tuple[list[tuple[int, int]], list[list[int]]]:
    # we want to only allow a union that doesn't change set one time
    same_set = False
    answers = []
    unions = []
    prev_state = disjoint_set.get_parent().copy()
    cur_state = prev_state
    for i in range(n):
        while prev_state == cur_state:
            C, H = random.randrange(num_sets), random.randrange(num_sets)
            while C == H:
                C = random.randrange(num_sets)
                H = random.randrange(num_sets)

            disjoint_set.union(C, H)
            cur_state = disjoint_set.get_parent().copy()

            if prev_state == cur_state:
                if same_set:  # if we have already had a union that doesn't change the set, we can't have another one
                    continue
                else:
                    same_set = True  # we have had a union that doesn't change the set, so we can't have another one
                    break
            break

        prev_state = cur_state
        unions.append((C, H))
        answers.append(cur_state)
    return unions, answers


# convert unions of the form [(5, 2), (6, 3), (8, 6)] into ["union(F,C)", "union(G,D)", "union(I,G)"]
def display_unions(unions: list[tuple[int, int]]) -> list[str]:
    return [
        "union({},{})".format(chr(ord("A") + first), chr(ord("A") + second))
        for first, second in unions
    ]


# function that takes in a list of states and returns what the next state would be with no path compression
def generate_no_pc_state(prev_state: list[int], union: tuple[int, int]) -> list[int]:
    dsu = DisjointSetUnion(len(prev_state), False, prev_state)
    dsu.union(*union)
    no_pc_state = dsu.get_parent()
    return no_pc_state


# parses union and returns the answers
def parse_and_run_union(
    union_list: list[tuple[int, int]], disjoint_set: DisjointSetUnion
) -> list[list[int]]:
    answers = []
    for union in union_list:
        disjoint_set.union(*union)
        answers.append(disjoint_set.get_parent().copy())
    return answers


def grade_current_row(data: su.QuestionData, attempts_allowed: int) -> None:
    current_row_number: int = data["params"]["current_row_number"]
    question_name = get_question_name("answer", data)
    student_answer: list[int] = convert_string_to_list(
        data["submitted_answers"][question_name]
    )

    current_row: RowDict = data["params"]["table_rows"][current_row_number]
    current_row["attempts"] += 1

    if student_answer == current_row["set_state"]:
        data["params"]["feedback"] = "Good job! Complete the next set union above."
        data["score"] = 1

    else:
        data["score"] = 0
        if current_row["attempts"] == attempts_allowed:
            data["params"]["feedback"] = (
                "You have used all of your attempts. The correct answer has been given. Please try the next row"
            )
            current_row["attempts"] += 1
            return
        answer_without_pc = generate_no_pc_state(
            data["params"]["current_state"], current_row["union"]
        )
        if student_answer == answer_without_pc:
            data["params"]["feedback"] = (
                "The state after the set union is incorrect. You appear to have forgotten to use path compression."
            )
        else:
            data["params"]["feedback"] = "The state after the set union is incorrect"


def set_row_finished(row_dict: RowDict) -> None:
    "Change row_dict to finished status. is_upcoming should already be false."
    row_dict["is_finished"] = True
    row_dict["is_current"] = False


def get_question_name(question_name: str, data: su.QuestionData) -> str:
    current_row_number: int = data["params"]["current_row_number"]
    return f"{current_row_number}-{question_name}"


def convert_list_to_string(items: list[int]) -> str:
    # convert list to string
    return ",".join(str(num) for num in items).strip()


def display_list(items: list[int]) -> str:
    # convert list to string put space before positive numbers
    return ",".join(str(num) if num < 0 else f" {num}" for num in items)


def clean_input(string: str) -> str:
    return (
        string.replace(" ", "")
        .replace("[", "")
        .replace("]", "")
        .replace("(", "")
        .replace(")", "")
        .strip()
    )


def convert_string_to_list(string: str) -> list[int]:
    return [int(num) for num in string.split(",")]


def get_mustache_path(data: QuestionData) -> str:
    return (
        data["options"]["server_files_course_path"]
        + "/theorielearn/disjoint_sets/question_base.mustache"
    )


def generate(
    data: QuestionData,
    pc: bool,
    n: int = 10,
    *,
    unions: Optional[list[tuple[int, int]]] = None,
    num_random_unions: Optional[int] = None,
) -> None:
    if pc:
        data["params"]["pc_description"] = "uses path compression"
    else:
        data["params"]["pc_description"] = "does not use path compression"

    # ensure that either unions or num_unions is specified bot not both
    if (unions and num_random_unions) or (not unions and not num_random_unions):
        raise ValueError("Either unions or num_unions must be specified, but not both")

    dsu = DisjointSetUnion(n, pc)
    if unions is not None:
        answers = parse_and_run_union(unions, dsu)
    else:
        if num_random_unions is not None:
            unions, answers = random_unions_diff_sets_with_answers(
                num_random_unions, dsu
            )

    if unions:
        row_table_list = generate_table_list(answers, unions)
    set_row_list_current(row_table_list, 0)

    data["params"]["table_rows"] = row_table_list
    data["params"]["current_row_number"] = 0

    data["params"]["current_state"] = [-1 for _ in range(n)]
    data["params"]["current_state_display"] = convert_list_to_string(
        data["params"]["current_state"]
    ).strip()

    with open(get_mustache_path(data)) as f:
        data["params"]["html"] = chevron.render(f, data["params"]).strip()


def grade(data: su.QuestionData, attempts_allowed: int = 3) -> None:
    data["params"]["last_submission_correct"] = True
    table_rows: list[RowDict] = data["params"]["table_rows"]
    current_row_number: int = data["params"]["current_row_number"]

    # Only do something if we haven't done the whole table yet
    if current_row_number < len(table_rows):
        # Grade current row
        grade_current_row(data, attempts_allowed)

        # Move on to custom grading
        if (
            data["score"] == 1
            or table_rows[current_row_number]["attempts"] > attempts_allowed
        ):
            # Use to set feedback for last submission correct

            data["params"]["last_submission_correct"] = True

            current_row = table_rows[current_row_number]

            # Set current row to be finished, and set future states that will be visited
            set_row_finished(current_row)
            # update current state to be equal to set state in current row
            data["params"]["current_state"] = current_row["set_state"]
            data["params"]["current_state_display"] = convert_list_to_string(
                current_row["set_state"]
            ).strip()

            current_row_number += 1

            data["params"]["current_row_number"] = current_row_number

            # If not finished, set next row to be current
            if current_row_number < len(table_rows):
                set_row_list_current(table_rows, current_row_number)

            # If finished, set done marker
            else:
                data["params"]["is_done"] = True

        else:
            # Use to set feedback for last submission incorrect
            data["params"]["last_submission_correct"] = False

    correct_rows = sum(
        1 if table_row["attempts"] <= attempts_allowed else 0
        for table_row in table_rows[:current_row_number]
    )

    data["score"] = correct_rows / len(table_rows)

    with open(get_mustache_path(data)) as f:
        data["params"]["html"] = chevron.render(f, data["params"]).strip()
