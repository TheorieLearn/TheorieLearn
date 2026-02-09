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


def getCorrectMaxProfit(
    profit: ArbitraryIndexArray[Tuple[int]],
    skip: ArbitraryIndexArray[Tuple[int]],
    n: int,
) -> MemoArray[Tuple[int]]:
    MaxProfit: MemoArray[Tuple[int]] = MemoArray(name="MaxProfit")
    MaxProfit.set_bounds((1, n))

    MaxProfit[n] = profit[n]
    for i in range(n - 1, 0, -1):
        if i + 1 + skip[i] > n:
            MaxProfit[i] = max(profit[i], MaxProfit[i + 1])
        else:
            MaxProfit[i] = max(
                profit[i] + MaxProfit[int(i + 1 + skip[i])], MaxProfit[i + 1]
            )

    return MaxProfit


def generate_test_data(p: np.ndarray, s: np.ndarray, n: int) -> Tuple:
    profit: ArbitraryIndexArray[Tuple[int]] = ArbitraryIndexArray(
        filled_arr=p, read_only=True, name="profit"
    )

    skip: ArbitraryIndexArray[Tuple[int]] = ArbitraryIndexArray(
        filled_arr=s, read_only=True, name="skip"
    )

    correct_arr = getCorrectMaxProfit(profit, skip, n)
    correct_ans = correct_arr[1]

    student_arr: MemoArray = MemoArray(name="MaxProfit")

    return profit, skip, correct_arr, correct_ans, student_arr


class Test(PLTestCase):
    @points(1)
    @name("Check example test case")
    def test_0(self) -> None:
        p = np.array([3, 7, 3, 5, 6, 4], dtype=np.int64)
        s = np.array([2, 0, 2, 3, 1, 2], dtype=np.int64)
        n = len(p)

        profit, skip, correct_arr, correct_ans, student_arr = generate_test_data(
            p, s, n
        )
        student_ans = Feedback.call_user(
            self.st.ComputeMaxProfit, profit, skip, n, student_arr
        )

        results = generate_student_feedback(
            {"profit": list(p), "skip": list(s)},
            student_ans,
            student_arr,
            correct_ans,
            correct_arr,
        )
        for i in results.feedback:
            Feedback.add_feedback(i)
        Feedback.set_score(results.grade)

    @points(10)
    @name("Check random profits and skips")
    def test_1(self) -> None:
        iter_num = 10
        lowest_grade = 1.0
        feedback = []
        for _ in range(iter_num):
            n = 10
            p = np.random.randint(low=0, high=10, size=n)
            s = np.random.randint(low=0, high=10, size=n)

            profit, skip, correct_arr, correct_ans, student_arr = generate_test_data(
                p, s, n
            )
            student_ans = Feedback.call_user(
                self.st.ComputeMaxProfit, profit, skip, n, student_arr
            )

            results = generate_student_feedback(
                {"profit": list(p), "skip": list(s)},
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
