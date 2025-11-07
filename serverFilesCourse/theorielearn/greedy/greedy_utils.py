from typing import Callable, List, Optional, Tuple, Union

import prairielearn as pl
import theorielearn.shared_utils as su
from numpy import allclose, isclose

StrategyT = Callable[[int, float, List[float], List[float]], List[float]]


def get_correct_advertisers(
    n: int, W: float, L: List[float], P: List[float]
) -> List[float]:
    """
    Produces the correct solution to the TV advertisers greedy problem.
    """
    return get_advertisers(n, W, L, P, lambda x: x[1] / x[0])


def get_advertisers(
    n: int,
    W: float,
    L: List[float],
    P: List[float],
    strategy: Callable[[Tuple[float, float, int]], Union[int, float]],
) -> List[float]:
    """
    Produces a solution (right or wrong) to the TV advertisers greedy problem
    based on the provided strategy
    """
    combined = list(zip(L, P, range(n)))
    combined.sort(key=strategy, reverse=True)

    X: List[float] = [0.0 for _ in range(n)]
    time_remaining = W
    for l, p, i in combined:
        if isclose(time_remaining, 0):
            break
        minutes = min(l, time_remaining)
        X[i] = minutes
        time_remaining -= minutes
    return X


def parse_advertiser_inputs(data: su.QuestionData, nums: List[str], lists: List[str]):
    """
    Parses inputs for the TV greedy problems. nums consists of a list of
    variable names for integer/float inputs, and lists consists of a
    list of variable names for comma-separated list inputs
    """

    # ensure nums are formatted correctly
    for num in nums:
        if num not in data["format_errors"]:
            if data["submitted_answers"][num] < 0:
                data["format_errors"][num] = (
                    rf"The value of ${num}$ must be non-negative.<br>"
                )

    # ensure lists are formatted correctly
    for lst in lists:
        if lst not in data["format_errors"]:
            try:
                # reformat into a list of floats
                data["submitted_answers"][lst] = list(
                    map(float, data["submitted_answers"][lst].split(","))
                )
            except ValueError:
                data["format_errors"][lst] = (
                    rf"${lst}$ must be a comma-separated list of numbers.<br>"
                )
                continue

            if lst == "L":
                if not all([x > 0 for x in data["submitted_answers"][lst]]):
                    data["format_errors"][lst] = (
                        rf"${lst}$ must be a comma-separated list of positive numbers.<br>"
                    )
            else:
                if not all([x >= 0 for x in data["submitted_answers"][lst]]):
                    data["format_errors"][lst] = (
                        rf"${lst}$ must be a comma-separated list of non-negative numbers.<br>"
                    )
            if (
                "n" not in data["format_errors"]
                and len(data["submitted_answers"][lst])
                != data["submitted_answers"]["n"]
            ):
                data["format_errors"][lst] = rf"${lst}$ must have length $n$.<br>"


def grade_advertisers(
    data: su.QuestionData,
    get_wrong_X: Callable[[int, float, List[float], List[float]], List[float]],
) -> None:
    """
    Grades a solution X to the TV advertisers greedy problem.
    """

    def grade_X(
        X: List[float], name: str, get_X_sol: StrategyT, data: su.QuestionData
    ) -> Tuple[bool, Optional[str]]:
        n = data["submitted_answers"]["n"]
        W = data["submitted_answers"]["W"]
        L = data["submitted_answers"]["L"]
        P = data["submitted_answers"]["P"]
        X_sol = get_X_sol(n, W, L, P)
        # accounts for case where the incorrect strategy does not provide a counterexample
        if not allclose(X, X_sol):
            return False, rf"${name}$ is incorrect.<br>"
        elif get_X_sol == get_wrong_X and X_sol == get_correct_advertisers(n, W, L, P):
            return (
                False,
                rf"${name}$ is incorrect. This is not a counterexample to the optimal strategy.<br>",
            )
        return True, None

    su.grade_question_parameterized(
        data, "X_w", lambda x: grade_X(x, "X_w", get_wrong_X, data)
    )
    su.grade_question_parameterized(
        data, "X_c", lambda x: grade_X(x, "X_c", get_correct_advertisers, data)
    )
    pl.set_weighted_score_data(data)
