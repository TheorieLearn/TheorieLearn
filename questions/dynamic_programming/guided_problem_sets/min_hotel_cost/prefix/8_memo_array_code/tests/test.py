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
    HotelCosts: ArbitraryIndexArray[Tuple[int]], n: int
) -> MemoArray[Tuple[int]]:
    correctMinCost: MemoArray[Tuple[int]] = MemoArray(name="MinCost")
    correctMinCost.set_bounds((1, n))

    correctMinCost[1] = 0
    correctMinCost[2] = HotelCosts[2]
    for i in range(3, n + 1):
        correctMinCost[i] = (
            min(correctMinCost[i - 1], correctMinCost[i - 2]) + HotelCosts[i]
        )
    return correctMinCost


def generate_test_data(costs: np.ndarray, n: int) -> Tuple:
    HotelCosts: ArbitraryIndexArray[Tuple[int]] = ArbitraryIndexArray(
        filled_arr=costs, read_only=True, name="HotelCosts"
    )

    correct_arr = getCorrectMinCost(HotelCosts, n)
    correct_ans = correct_arr[n]

    student_arr: MemoArray = MemoArray(name="MinCost")

    return HotelCosts, correct_arr, correct_ans, student_arr


class Test(PLTestCase):
    @points(1)
    @name("Check example answer")
    def test_0(self) -> None:
        costs = np.array([0, 1, 374, 3, 0])
        n = len(costs)

        HotelCosts, correct_arr, correct_ans, student_arr = generate_test_data(costs, n)
        student_ans = Feedback.call_user(
            self.st.ComputeMinTotalCost, HotelCosts, n, student_arr
        )

        results = generate_student_feedback(
            {"HotelCosts": list(costs)},
            student_ans,
            student_arr,
            correct_ans,
            correct_arr,
        )
        for i in results.feedback:
            Feedback.add_feedback(i)
        Feedback.set_score(results.grade)

    @points(10)
    @name("Check small random hotel costs")
    def test_1(self) -> None:
        iter_num = 10
        lowest_grade = 1.0
        feedback = []
        for _ in range(iter_num):
            n = 10
            costs = np.random.randint(10, size=n)
            costs[0] = 0
            costs[n - 1] = 0

            HotelCosts, correct_arr, correct_ans, student_arr = generate_test_data(
                costs, n
            )
            student_ans = Feedback.call_user(
                self.st.ComputeMinTotalCost, HotelCosts, n, student_arr
            )

            results = generate_student_feedback(
                {"HotelCosts": list(costs)},
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
