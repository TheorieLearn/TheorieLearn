from typing import List, Tuple

import numpy as np
import pytest
from theorielearn.dynamic_programming.arbitrary_index_array import ArbitraryIndexArray
from theorielearn.dynamic_programming.dp_coding_exception import DPCodingException
from theorielearn.dynamic_programming.memo_array import MemoArray
from theorielearn.dynamic_programming.utils import NAN_ANSWER_FEEDBACK, generate_student_feedback


class VerifyArbitraryIndexArray:
    @pytest.mark.parametrize(
        "sample, bounds",
        [
            (np.array([1]), [(1, 1)]),
            (np.array([[1]]), [(1, 1), (1, 1)]),
            (np.array([[1, 2], [3, 4]]), [(1, 2), (1, 2)]),
            (
                np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]),
                [(1, 2), (1, 2), (1, 3)],
            ),
        ],
    )
    def verify_init_bounds_w_arr(
        self, sample: np.ndarray, bounds: List[Tuple[int, int]]
    ) -> None:
        x: ArbitraryIndexArray = ArbitraryIndexArray(filled_arr=sample)
        assert x.bounds == bounds

    @pytest.mark.parametrize(
        "sample",
        [
            (np.array([1])),
            (np.array([[1]])),
            (np.array([[1, 2], [3, 4]])),
            (np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])),
        ],
    )
    def verify_set_bounds(self, sample: np.ndarray) -> None:
        with pytest.raises(DPCodingException) as excinfo:
            x: ArbitraryIndexArray = ArbitraryIndexArray(
                filled_arr=sample, read_only=True
            )
            x.set_bounds((0, 5))
        assert "Bounds cannot be changed in a read-only array." in str(excinfo.value)

        with pytest.raises(DPCodingException) as excinfo:
            x = ArbitraryIndexArray()
            x.set_bounds(1)  # type: ignore
            x.set_bounds(1, 2)  # type: ignore
            x.set_bounds(1, 2, (3, 4))  # type: ignore
        assert "Bounds must be given as tuples." in str(excinfo.value)

        x.set_bounds((1, 5))
        assert x.bounds == [(1, 5)]
        x.set_bounds((1, 5), (1, 4))
        assert x.bounds == [(1, 5), (1, 4)]

    def verify_check_type_bounds(self) -> None:
        x: ArbitraryIndexArray[Tuple[int]] = ArbitraryIndexArray(name="x")
        y = None

        # test exceptions
        with pytest.raises(DPCodingException) as excinfo:
            x[0] = 1
        assert "You must first set the bounds of the array" in str(excinfo.value)

        # test idx type exception
        with pytest.raises(DPCodingException) as excinfo:
            x.set_bounds((0, 1), (0, 1))
            y = x[0]
        assert "Your code attempted to access x[0], but x is 2-D." in str(excinfo.value)
        assert y == None

        with pytest.raises(DPCodingException) as excinfo:
            x.set_bounds((0, 1))
            x[0, 1] = 4
        assert "Your code attempted to access x[0, 1], but x is 1-D." in str(
            excinfo.value
        )

        # test idx out of bounds exception
        with pytest.raises(DPCodingException) as excinfo:
            x.set_bounds((1, 2))
            y = x[3]
        assert (
            "Your code attempted to access x[3], but you set your array bounds as x[(1, 2)]."
            in str(excinfo.value)
        )
        assert y == None

        with pytest.raises(DPCodingException) as excinfo:
            x.set_bounds((1, 2), (3, 5))
            x[3, 6] = 4
        assert (
            "Your code attempted to access x[3, 6], but you set your array bounds as x[(1, 2), (3, 5)]."
            in str(excinfo.value)
        )

    @pytest.mark.parametrize(
        "filled",
        [
            (np.array([1])),
            (np.array([[1]])),
            (np.array([[1, 2], [3, 4]])),
            (np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])),
        ],
    )
    def verify_getitem(self, filled: np.ndarray) -> None:
        # test exception
        x: ArbitraryIndexArray = ArbitraryIndexArray(name="x")
        x.set_bounds((0, 4))
        y = None
        with pytest.raises(DPCodingException) as excinfo:
            y = x[0]
        assert (
            "Your code tried to access x[0], but this has not yet been evaluated yet."
            in str(excinfo.value)
        )
        assert y == None

        # test correct
        x = ArbitraryIndexArray(filled_arr=filled)
        for idx, val in np.ndenumerate(filled):
            one_indexed = tuple(map(lambda x: x + 1, idx))
            if len(idx) == 1:  # ndenumerate gives tuple even if int, cast accordingly
                y = x[one_indexed[0]]
            else:
                y = x[one_indexed]
            assert y == val

    @pytest.mark.parametrize(
        "filled, test_idx",
        [
            (np.array([1]), 1),
            (np.array([[1]]), (1, 1)),
            (np.array([[1, 2], [3, 4]]), (1, 1)),
            (np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]), (1, 1, 1)),
        ],
    )
    def verify_setitem(self, filled: np.ndarray, test_idx: Tuple[int, ...]) -> None:
        # test read-only
        x: ArbitraryIndexArray = ArbitraryIndexArray(
            filled_arr=filled, name="x", read_only=True
        )
        with pytest.raises(DPCodingException) as excinfo:
            x[test_idx] = 2
        assert "The array x is set as read only." in str(excinfo.value)

        # test correct
        y: ArbitraryIndexArray = ArbitraryIndexArray(
            filled_arr=filled, name="x", read_only=False
        )
        y[test_idx] = 10000
        assert y[test_idx] == 10000

    @pytest.mark.parametrize(
        "filled, test_idx",
        [
            (np.array([1]), (1,)),
            (np.array([[1]]), (1, 1)),
            (np.array([[1, 2], [3, 4]]), (1, 1)),
            (np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]), (1, 1, 1)),
        ],
    )
    def verify_diff(self, filled: np.ndarray, test_idx: Tuple[int, ...]) -> None:
        x: ArbitraryIndexArray = ArbitraryIndexArray(name="x")
        y: ArbitraryIndexArray = ArbitraryIndexArray(filled_arr=filled, name="y")

        x.set_bounds((1, 3), (1, 3))
        diff = x.diff(y)
        assert diff.same_bounds is False

        x = ArbitraryIndexArray(filled_arr=filled, name="x")
        x[test_idx] = 1000
        diff = x.diff(y)
        assert test_idx == diff.first_wrong_val

        x.entries.pop(test_idx)
        diff = x.diff(y)
        assert [test_idx] == diff.uninitialized


class VerifyMemoArray:
    def verify_setitem(self) -> None:
        x: MemoArray = MemoArray(name="x")
        x.set_bounds((0, 4))

        with pytest.raises(DPCodingException) as excinfo:
            x[1] = x[2] + x[3]
        assert (
            "When evaluating x[1], your code tried to access the following uninitialized entries: ['x[2]', 'x[3]']"
            in str(excinfo.value)
        )

        x.set_bounds((0, 4), (1, 3))
        with pytest.raises(DPCodingException) as excinfo:
            x[1, 3] = x[1, 1] + x[2, 2] + x[0, 1]
        assert (
            "When evaluating x[1, 3], your code tried to access the following uninitialized entries: ['x[1, 1]', 'x[2, 2]', 'x[0, 1]']"
            in str(excinfo.value)
        )


def verify_generate_student_feedback_nan_answer() -> None:
    feedback = generate_student_feedback(
        dict(), np.nan, MemoArray(name="x"), 0, MemoArray(name="y"), False
    )
    assert feedback.grade == 0
    assert feedback.feedback == [NAN_ANSWER_FEEDBACK]
