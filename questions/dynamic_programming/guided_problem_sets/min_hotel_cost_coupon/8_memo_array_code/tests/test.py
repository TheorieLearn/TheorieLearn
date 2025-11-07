import sys
from typing import Tuple

import numpy as np
from code_feedback import Feedback
from theorielearn.dynamic_programming.arbitrary_index_array import ArbitraryIndexArray
from theorielearn.dynamic_programming.memo_array import MemoArray
from theorielearn.dynamic_programming.utils import generate_student_feedback
from pl_helpers import name, points
from pl_unit_test import PLTestCase

sys.path.insert(1, "/grade/serverFilesCourse")


def getCorrectMinCost(
    HotelCosts: ArbitraryIndexArray[Tuple[int]], n: int, k: int
) -> MemoArray[Tuple[int, int]]:
    correctMinCost: MemoArray[Tuple[int, int]] = MemoArray(name="MinCost")
    correctMinCost.set_bounds((1, n), (0, k))

    def evaluate_subproblem(i, j):
        if i == n:
            return 0
        elif i == n - 1 and j == 0:
            return HotelCosts[i]
        elif i == n - 1 and j > 0:
            return 0
        elif j == 0:
            return min(
                HotelCosts[i] + correctMinCost[i + 1, j],
                HotelCosts[i] + correctMinCost[i + 2, j],
            )
        else:
            return min(
                HotelCosts[i] + correctMinCost[i + 1, j],
                HotelCosts[i] + correctMinCost[i + 2, j],
                correctMinCost[i + 1, j - 1],
                correctMinCost[i + 2, j - 1],
            )

    for i in reversed(range(1, n + 1)):
        for j in range(0, k + 1):
            correctMinCost[i, j] = evaluate_subproblem(i, j)

    return correctMinCost


def generate_test_data(costs: np.ndarray, n: int, k: int) -> Tuple:
    HotelCosts: ArbitraryIndexArray[Tuple[int]] = ArbitraryIndexArray(
        filled_arr=costs, read_only=True, name="HotelCosts"
    )

    correct_arr = getCorrectMinCost(HotelCosts, n, k)
    correct_ans = correct_arr[1, k]
    student_arr: MemoArray = MemoArray(name="MinCost")

    return HotelCosts, correct_arr, correct_ans, student_arr


class Test(PLTestCase):
    @points(1)
    @name("Check example case 1")
    def test_0(self) -> None:
        costs = np.array([0, 126, 225, 1, 374, 3, 0])
        n = len(costs)
        k = 1

        HotelCosts, correct_arr, correct_ans, student_arr = generate_test_data(
            costs, n, k
        )
        student_ans = Feedback.call_user(
            self.st.ComputeMinTotalCost, HotelCosts, n, k, student_arr
        )

        results = generate_student_feedback(
            {"HotelCosts": list(costs), "k": k},
            student_ans,
            student_arr,
            correct_ans,
            correct_arr,
        )
        for i in results.feedback:
            Feedback.add_feedback(i)

        Feedback.set_score(results.grade)

    @points(1)
    @name("Check example case 2")
    def test_1(self) -> None:
        costs = np.array([0, 126, 225, 1, 374, 3, 0])
        n = len(costs)
        k = 2

        HotelCosts, correct_arr, correct_ans, student_arr = generate_test_data(
            costs, n, k
        )
        student_ans = Feedback.call_user(
            self.st.ComputeMinTotalCost, HotelCosts, n, k, student_arr
        )

        results = generate_student_feedback(
            {"HotelCosts": list(costs), "k": k},
            student_ans,
            student_arr,
            correct_ans,
            correct_arr,
        )
        for i in results.feedback:
            Feedback.add_feedback(i)
        Feedback.set_score(results.grade)

    @points(10)
    @name("Check random hotel costs")
    def test_2(self) -> None:
        iter_num = 10
        lowest_grade = 1.0
        feedback = []
        for _ in range(iter_num):
            n = 10
            k = np.random.randint(2, 4)
            costs = np.random.randint(10, size=n)
            costs[0] = 0
            costs[n - 1] = 0

            HotelCosts, correct_arr, correct_ans, student_arr = generate_test_data(
                costs, n, k
            )
            student_ans = Feedback.call_user(
                self.st.ComputeMinTotalCost, HotelCosts, n, k, student_arr
            )

            results = generate_student_feedback(
                {"HotelCosts": list(costs), "k": k},
                student_ans,
                student_arr,
                correct_ans,
                correct_arr,
            )

            # Print feedback for the lowest scoring test case
            if results.grade < lowest_grade:
                lowest_grade = results.grade
                feedback = results.feedback

        for i in feedback:
            Feedback.add_feedback(i)
        Feedback.set_score(lowest_grade)


Test.total_iters = 1
