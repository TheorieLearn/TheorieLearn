import itertools
import re
import string
from typing import Callable, Iterable

import theorielearn.shared_utils as su
from nltk.grammar import Nonterminal

from theorielearn.scaffolded_writing.cfg import ScaffoldedWritingCFG
from theorielearn.scaffolded_writing.student_submission import StudentSubmission

POTENTIAL_VARIABLE_NAMES = set(string.ascii_lowercase) - {"a"}


class DPStudentSubmission(StudentSubmission):
    def __init__(self, token_list: list[str], cfg: ScaffoldedWritingCFG) -> None:
        super().__init__(token_list, cfg)

        self.func_name: str | None = None
        self.func_params: set[str] = set()

        (function_declaration_subtree,) = self.parse_tree.subtrees(
            filter=lambda subroot: subroot.label() == "FUNCTION_DECLARATION"
        )
        (function_declaration,) = function_declaration_subtree
        assert isinstance(function_declaration, str)

        match = re.fullmatch(r"(.+)\((.+)\)", function_declaration)
        if match is not None:
            self.func_name = match.group(1)
            self.func_params = set(match.group(2).replace(" ", "").split(","))

        # The set of all one-letter variables which are mentioned in the student's response
        # outside of the function_declaration.
        self.mentioned_variables: set[str] = set.union(
            *(
                self.__extract_variables(token)
                for token in self.token_list
                if token != function_declaration
            )
        )

    def get_parameters_in_field(self, field_label: str) -> set[str]:
        assert Nonterminal(field_label) in self.cfg.nonterminals

        subtrees = list(
            self.parse_tree.subtrees(
                filter=lambda subroot: subroot.label() == field_label
            )
        )
        if len(subtrees) == 0:
            return set()

        (field_subtree,) = subtrees
        (field_value,) = field_subtree.leaves()

        return self.__extract_variables(field_value).intersection(self.func_params)

    def is_field_value_parameterized(self, field_label: str) -> bool:
        """
        field_label is the nonterminal that generates the field value
        """
        return len(self.get_parameters_in_field(field_label)) > 0

    @staticmethod
    def __extract_variables(token: str) -> set[str]:
        return POTENTIAL_VARIABLE_NAMES.intersection(re.split(r"\W+", token))


ConstraintT = Callable[[DPStudentSubmission], str | None]


def declare_func_constraint() -> ConstraintT:
    def constraint(submission: DPStudentSubmission) -> str | None:
        if submission.func_name is not None:
            return None

        return "Your subproblem definition should declare a function with input parameters that can be memoized."

    return constraint


def correct_noun_and_adj_constraint(correct_noun: str, correct_adj: str) -> ConstraintT:
    def constraint(submission: DPStudentSubmission) -> str | None:
        is_noun_correct = submission.does_path_exist("OUTPUT_NOUN", correct_noun)
        is_adj_correct = submission.does_path_exist("EXTREMAL_ADJ", correct_adj)

        if is_noun_correct and is_adj_correct:
            return None

        if submission.does_path_exist("OUTPUT_NOUN", "answer"):
            return 'Please be more precise about what quantity the function actually outputs. Just saying "answer" is too vague.'

        if is_noun_correct and submission.does_path_exist("EXTREMAL_ADJ", "EPSILON"):
            return f'The {correct_noun} can vary based on what choices we make. You need to add an adjective in front of "{correct_noun}" in order to precisely define the output quantity of the function.'

        return "It seems like the quantity outputted by your function is not directly relevant for solving the original problem."

    return constraint


def descriptive_func_name_constraint(correct_func_name: str) -> ConstraintT:
    def constraint(submission: DPStudentSubmission) -> str | None:
        if submission.func_name == correct_func_name:
            return None

        return "Please choose a descriptive function name that accurately represents what the function outputs."

    return constraint


def explain_params_constraint(variables_in_problem: set[str]) -> ConstraintT:
    def constraint(submission: DPStudentSubmission) -> str | None:
        unexplained_params = submission.func_params - submission.mentioned_variables
        undefined_variables = (
            submission.mentioned_variables
            - submission.func_params
            - variables_in_problem
        )
        mentioned_params_without_explaining = submission.does_path_exist(
            "MENTION_PARAMS_WITHOUT_EXPLAINING"
        )

        if not (
            unexplained_params
            or undefined_variables
            or mentioned_params_without_explaining
        ):
            return None

        if unexplained_params:
            if len(unexplained_params) == 1:
                return f"Your function takes {su.list_to_english(sorted(unexplained_params))} as an input parameter, but your subproblem definition does not explain how this parameter affects the output of the function."
            else:
                return f"Your function takes {su.list_to_english(sorted(unexplained_params))} as input parameters, but your subproblem definition does not explain how these parameters affect the output of the function."
        if undefined_variables:
            if len(undefined_variables) == 1:
                return f"Your subproblem definition refers to the variable {su.list_to_english(sorted(undefined_variables))}, which is undefined. You should only refer to variables which are defined in the original problem or declared as input parameters to your function."
            else:
                return f"Your subproblem definition refers to the variables {su.list_to_english(sorted(undefined_variables))}, which are undefined. You should only refer to variables which are defined in the original problem or declared as input parameters to your function."

        if mentioned_params_without_explaining:
            return "Your subproblem definition mentions the function's input parameters, but it does not clearly explain how these input parameters affect the output of the function. Can you be more specific about what the function parameters represent in the context of your subproblem?"

        raise Exception("This constraint was violated but no feedback was generated.")

    return constraint


def decoupled_parameters_constraint(**independent_fields: str) -> ConstraintT:
    def constraint(
        submission: DPStudentSubmission,
    ) -> str | None:
        """
        independent_fields: the values in these fields should not contain the same parameters
            - key = the nonterminal assosciated with the field
            - value = an English description of the field
            (This dict should have length at least 2 in order to be meaningful.)
        """
        assert len(independent_fields) >= 2

        for (field1, description1), (field2, description2) in itertools.combinations(
            independent_fields.items(), 2
        ):
            intersection = submission.get_parameters_in_field(field1).intersection(
                submission.get_parameters_in_field(field2)
            )

            if intersection:
                (overused_param,) = intersection
                entangled_quantities = (description1, description2)
                return f"You used the parameter {overused_param} to denote both {entangled_quantities[0]} and {entangled_quantities[1]}. It doesn't make sense to tie both of these quantities to the same parameter because these quantities can vary independently."

        return None

    return constraint


def can_compute_final_answer_constraint(
    *required_feature: str, feedback_elaboration: str
) -> ConstraintT:
    def constraint(submission: DPStudentSubmission) -> str | None:
        """
        required_feature is a path that must be present in order to compute the final answer
        """
        if submission.does_path_exist(*required_feature):
            return None

        return f"Your subproblem definition does not allow us to compute the final answer requested by the original problem. The problem requires that {feedback_elaboration}, but there is no way to impose this requirement using your subproblem definition."

    return constraint


def reduces_recursively_constraint(
    field_requiring_parameters: str,
    get_unhandled_scenario: Callable[[DPStudentSubmission], str],
) -> ConstraintT:
    if not field_requiring_parameters.isupper():
        raise ValueError("field_requiring_parameters was not a CFG Rule token")

    def constraint(submission: DPStudentSubmission) -> str | None:
        if submission.is_field_value_parameterized(field_requiring_parameters):
            return None

        return f"Make sure that your subproblem can be reduced to smaller instances of itself. For example, {get_unhandled_scenario(submission)}, but your subproblem definition does not allow us to do that."

    return constraint


def no_irrelevant_restrictions_constraint(*irrelevant_features: str) -> ConstraintT:
    def constraint(submission: DPStudentSubmission) -> str | None:
        if all(
            not submission.does_path_exist(feature) for feature in irrelevant_features
        ):
            return None

        return "Your subproblem definition contains features or restrictions that are not relevant for solving the original problem."

    return constraint


def no_double_ended_parameterization_constraint() -> ConstraintT:
    def constraint(submission: DPStudentSubmission) -> str | None:
        if not submission.does_path_exist("DOUBLE_ENDED_SUBPROBLEM"):
            return None

        return "You parametrized both the start and end index of your subproblem, but for this problem, your subproblem doesn't need to reduce on both sides. Each possible choice should only cause your subproblem to get smaller on one side. Your subproblem definition might still be viable, but this slows down your algorithm by a factor of $O(n)$. (Some other problems actually do require reducing on both sides, e.g. see the Longest Palindromic Subsequence problem from lab.)"

    return constraint


def misc_constraint(
    field_requiring_parameters: str,
    get_unhandled_scenario: Callable[[DPStudentSubmission], str],
) -> ConstraintT:
    if not field_requiring_parameters.isupper():
        raise ValueError("field_requiring_parameters was not a CFG Rule token")

    def constraint(submission: DPStudentSubmission) -> str | None:
        if submission.is_field_value_parameterized(field_requiring_parameters):
            return None

        return get_unhandled_scenario(submission)

    return constraint


# Constraint Helper Functions


def concat_into_production_rule(*iterables: Iterable[str]) -> str:
    """
    concat_into_production_rule([a1, a2, a3], [b1, b2], [c1, c2]) will return:
    "a1b1c1" | "a1b1c2" | "a1b2c1" | "a1b2c2" | ...
    """

    def wrap_in_quotes(s: str) -> str:
        if '"' not in s:
            return f'"{s}"'
        elif "'" not in s:
            return f"'{s}'"
        raise Exception(
            f"Cannot wrap {s} in quotes because it already contains single and double quotes."
        )

    rhs_possibilities = [
        wrap_in_quotes("".join(tup)) for tup in itertools.product(*iterables)
    ]
    return " | ".join(rhs_possibilities)
