import random
from typing import Any, Type, cast

import prairielearn.sympy_utils as phs
import sympy
from numpy.random import choice, randint
from theorielearn.shared_utils import QuestionData, grade_question_parameterized

PARSING_ERROR_MSG = "We were unable to parse your expression. Check for syntax errors \
    and make sure to only use the listed valid variables/functions."


class SympyGrader:
    MATH_FUNCTIONS: dict[str, sympy.Function | Type[sympy.Min] | Type[sympy.Max]] = {
        "min": sympy.Min,
        "max": sympy.Max,
        "cos": sympy.cos,
        "sin": sympy.sin,
        "tan": sympy.tan,
        "arccos": sympy.acos,
        "arcsin": sympy.asin,
        "arctan": sympy.atan,
        "acos": sympy.acos,
        "asin": sympy.asin,
        "atan": sympy.atan,
        "arctan2": sympy.atan2,
        "atan2": sympy.atan2,
        "exp": sympy.exp,
        "log": sympy.log,
        "sqrt": sympy.sqrt,  # type: ignore
    }

    def __init__(
        self,
        question_name: str,
        local_functions: dict[str, int],
        local_variables: set[str],
        *,
        allow_math_functions: bool = True,
    ) -> None:
        self.question_name = question_name
        self.local_functions = local_functions
        self.local_variables = local_variables

        variables = {v: sympy.Symbol(v) for v in self.local_variables}
        functions = {f: sympy.Function(f) for f in self.local_functions}

        # TODO throw exception if input function conflicts with builtin math one
        if allow_math_functions:
            functions.update(self.MATH_FUNCTIONS)

        self.locals_for_eval: dict[str, dict[str, Any]] = {
            "functions": functions,
            "variables": variables,
            "helpers": {
                "_Integer": sympy.Integer,
            },
        }

        # Empty dicts for feedback
        self.specific_errors_feedback: dict[str, str] = dict()
        self.missing_func_feedback: dict[str, str] = dict()
        self.included_func_feedback: dict[str, str] = dict()

        self.func_with_argument_feedback: dict[str, dict[str, str]] = {
            func: dict() for func in self.local_functions
        }

        self.func_without_argument_feedback: dict[str, dict[str, str]] = {
            func: dict() for func in self.local_functions
        }

        self.has_graded = False

    def string_to_sympy(
        self,
        str_to_evaluate: str,
        substitutions: list[tuple[sympy.Expr, sympy.Expr]] = [],
    ) -> sympy.Expr:
        """
        Evaluates str_to_evaluate on the local functions and variables from this class.
        Makes substitutions based on the substitutions list of (value, substitution) pairs.
        """
        try:
            evaluated_str = phs.evaluate(str_to_evaluate, self.locals_for_eval)
            for var, sub in substitutions:
                evaluated_str = evaluated_str.subs(var, sub)
        except phs.HasInvalidFunctionError as err:
            function_name = err.text
            if function_name in self.local_variables:
                raise ValueError(
                    f"Variable '{function_name}' cannot be called as a function."
                )
            else:
                raise ValueError(
                    f"Function '{function_name}' is not defined for this question"
                )
        except phs.HasInvalidVariableError as err:
            variable_name = err.text
            if variable_name in self.local_functions:
                raise ValueError(
                    f"Function '{variable_name}' cannot be used as a variable."
                )
            else:
                raise ValueError(
                    f"Variable '{variable_name}' is not defined for this question"
                )
        except phs.HasEscapeError:
            raise ValueError(r"Answer cannot contain '\\'")
        except phs.HasCommentError:
            raise ValueError(r"Answer cannot contain '#'")
        except Exception:
            raise ValueError(PARSING_ERROR_MSG)

        # Check that all functions are called with the correct number of arguments
        for func_obj in evaluated_str.atoms(sympy.Function):
            func_name = str(func_obj.func)
            num_args = len(func_obj.args)

            if func_name in self.local_functions:
                expected_num_args = self.local_functions[func_name]

                if expected_num_args != num_args:
                    arguments_str = (
                        "argument" if expected_num_args == 1 else "arguments"
                    )
                    raise ValueError(
                        f"Function '{func_name}' must be invoked with"
                        f" {expected_num_args} {arguments_str}, not {num_args}."
                    )

        return evaluated_str

    def answer_includes_specific_errors_feedback(
        self, incorrect_answer: str, feedback: str
    ) -> None:
        """
        Give feedback if student submission has specific errors.
        """
        self.check_if_question_graded()

        self.specific_errors_feedback[incorrect_answer] = feedback

    def answer_not_includes_function_feedback(
        self, function: str, feedback: str
    ) -> None:
        """
        Give feedback if student submission does not include given function.
        """
        self.check_if_question_graded()

        if function not in self.local_functions:
            raise ValueError(f"Function {function} is not defined.")

        self.missing_func_feedback[function] = feedback

    def answer_includes_function_feedback(self, function: str, feedback: str) -> None:
        """
        Give feedback if student submission includes given function.
        """
        self.check_if_question_graded()

        if function not in self.local_functions:
            raise ValueError(f"Function {function} is not defined.")

        self.included_func_feedback[function] = feedback

    def answer_function_with_argument_feedback(
        self, function: str, argument: str, feedback: str
    ) -> None:
        """
        Give feedback if student submission includes given function
        called with the given argument.
        """
        self.check_if_question_graded()

        if function not in self.local_functions:
            raise ValueError(f"Function {function} is not defined.")

        self.func_with_argument_feedback[function][argument] = feedback

    def answer_function_without_argument_feedback(
        self, function: str, argument: str, feedback: str
    ) -> None:
        """
        Give feedback if student submission includes given function
        called without the given argument.
        """
        self.check_if_question_graded()

        if function not in self.local_functions:
            raise ValueError(f"Function {function} is not defined.")

        self.func_without_argument_feedback[function][argument] = feedback

    def check_if_question_graded(self) -> None:
        "Raise an exception if this question has already been graded"

        if self.has_graded:
            raise ValueError(
                f"Symbolic question '{self.question_name}' has already been graded"
            )

    def grade_question(
        self,
        data: QuestionData,
        *correct_answers: str,
        incorrect_answers: list[str] = [],
        substitutions: list[tuple[str, str]] = [],
    ) -> None:
        """
        For expressions using sympy, takes in data, the question name, student answer,
        correct answers, and local functions and variables as strings and grades the
        question in the data dictionary.
        """

        self.check_if_question_graded()

        self.has_graded = True

        # Parse all substitutions and answers and raise exception if any answers are invalid
        subs = [
            (self.string_to_sympy(var), self.string_to_sympy(substitute))
            for var, substitute in substitutions
        ]

        valid_answers = [
            self.string_to_sympy(s, substitutions=subs) for s in correct_answers
        ]

        # Define grade function for use in parameterized grader
        def grade(student_answer_str: str) -> tuple[bool, str | None]:
            student_expr = self.string_to_sympy(student_answer_str, substitutions=subs)

            for specfic_error in self.specific_errors_feedback:
                if student_expr == self.string_to_sympy(
                    specfic_error, substitutions=subs
                ):
                    return False, self.specific_errors_feedback[specfic_error]

            if any(student_expr == ans_expr for ans_expr in valid_answers):
                return True, None

            student_expr_no_subs = self.string_to_sympy(student_answer_str)
            used_functions: set[str] = set()

            # If incorrect, first go through and check how functions are invoked
            for func_obj in student_expr_no_subs.atoms(sympy.Function):
                func_name = str(func_obj.func)

                # If function is in the forbidden function list, return feedback
                if func_name in self.included_func_feedback:
                    return False, self.included_func_feedback[func_name]

                used_functions.add(func_name)

            # Give feedback based on which functions are missing
            for func, feedback in self.missing_func_feedback.items():
                if func not in used_functions:
                    return False, feedback

            # Once all functions are correct, then check their arguments
            for func_obj in student_expr_no_subs.atoms(sympy.Function):
                seen_arguments = set()
                function = str(func_obj.func)

                if function in self.func_with_argument_feedback:
                    for func_arg in func_obj.args:
                        argument = str(func_arg)

                        # Add to seen arguments list
                        seen_arguments.add(argument)

                        # Get feedback for the specific argument
                        if argument in self.func_with_argument_feedback[function]:
                            return False, self.func_with_argument_feedback[function][
                                argument
                            ]

                if function in self.func_without_argument_feedback:
                    for func_arg in self.func_without_argument_feedback[function]:
                        if func_arg not in seen_arguments:
                            return False, self.func_without_argument_feedback[function][
                                func_arg
                            ]

            return False, None

        grade_question_parameterized(data, self.question_name, grade)


def make_random_function(
    target_complexity: float = 1.0,
    base_expr_pair_passed: tuple[
        sympy.Expr, float
    ] = None,  # (base_expr, recursion_complexity)
    max_exponential: int = 5,  # Default to 5 exponential should not limit the normal generation
) -> tuple[sympy.Expr, sympy.Expr, sympy.Expr]:
    """
    Generates a random function both in a recursive form and in an expanded form
    Arguments:
        target_complexity: float, the target difficulty of the desired question
        base_expr_pair_passed: tuple[sympy.Expr, float], the custom base expression and its recursion complexity
        max_exponential: int, the maximum number of exponential allowed
    returns tuple f_recursive: sympy.Expr, f_evaluated: sympy.Expr, base_expr: sympy.Expr
    """

    x, y, z = sympy.symbols("x y z")
    f = sympy.symbols("f", cls=sympy.Function)
    local_symbols = [x, y, z]

    # base_expr_pairs is a list of (base_expr, recursion_complexity)
    base_expr_pairs = [
        (x**2, 0.5),
        (x + 1, 0.5),
        (2**x, 0.65),
    ]

    base_expr_pair = (
        random.choice(base_expr_pairs)
        if base_expr_pair_passed is None
        else base_expr_pair_passed
    )
    base_expr, recursion_complexity = base_expr_pair
    is_expr_exponential = not base_expr.is_polynomial(x)

    def f_eval(param: sympy.Expr) -> sympy.Expr:
        return base_expr.subs(x, param)

    GenerateT = tuple[sympy.Expr, sympy.Expr]

    def recursive_generate(
        cur_complexity: float, current_recursion: int
    ) -> tuple[sympy.Expr, sympy.Expr]:
        if cur_complexity >= target_complexity:
            res = randint(2, 5) * choice(local_symbols)
            return (res, res)

        # Calculate the probability for next expression
        probability = []
        if cur_complexity >= target_complexity * 3 / 4:
            if is_expr_exponential and current_recursion >= max_exponential:
                probability = [0.2, 0.3, 0.3, 0.2, 0.0]
            else:
                probability = [0.1, 0.25, 0.25, 0.15, 0.25]
        else:
            if is_expr_exponential and current_recursion >= max_exponential:
                probability = [0.0, 0.35, 0.35, 0.3, 0.0]
            else:
                probability = [0.0, 0.25, 0.25, 0.15, 0.35]

        option = choice(
            ["literal", "add-expression", "mul-expression", "power", "recursion"],
            p=probability,
        )

        if option == "literal":
            res = randint(1, 10) * choice(local_symbols)
            return (res, res)

        elif option == "add-expression":
            return cast(
                GenerateT,
                tuple(
                    map(
                        sympy.Add,
                        recursive_generate(cur_complexity + 0.4, current_recursion),
                        recursive_generate(cur_complexity + 0.4, current_recursion),
                    )
                ),
            )
        elif option == "mul-expression":
            return cast(
                GenerateT,
                tuple(
                    map(
                        sympy.Mul,
                        recursive_generate(cur_complexity + 0.4, current_recursion),
                        recursive_generate(cur_complexity + 0.4, current_recursion),
                    )
                ),
            )
        elif option == "power":
            return cast(
                GenerateT,
                tuple(
                    map(
                        lambda x: pow(x, 2),
                        recursive_generate(cur_complexity + 0.5, current_recursion),
                    )
                ),
            )
        else:
            next_level, next_level_eval = recursive_generate(
                cur_complexity + recursion_complexity, current_recursion + 1
            )
            res = f(next_level)
            eval_res = f_eval(next_level_eval)
            return res, eval_res

    main_result, main_result_eval = recursive_generate(
        0, 1
    )  # base recursion level is 1

    return f(main_result), f_eval(main_result_eval), base_expr
