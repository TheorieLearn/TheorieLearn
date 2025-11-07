from __future__ import annotations

from collections import OrderedDict
from typing import (
    Generic,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
)

import numpy as np
from typing_extensions import assert_never

from theorielearn.dynamic_programming.dp_coding_exception import DPCodingException

IndexBoundT = Tuple[int, ...]
IndexT = TypeVar("IndexT", bound=IndexBoundT)
InputIdxT = Union[int, IndexT]
ElementT = Union[float, int, bool]


class DiffDescription(NamedTuple):
    "A named tuple for the description of the differences for student feedback"

    same_bounds: bool
    uninitialized: Sequence[IndexBoundT]
    first_wrong_val: Optional[IndexBoundT]


class ArbitraryIndexArray(Generic[IndexT]):
    """
    Represents an array with arbitrary indices for guided dynamic programming problems
    """

    def __init__(
        self,
        filled_arr: Optional[np.ndarray] = None,
        read_only: bool = False,
        name: str = "arr",
    ) -> None:
        self.name = name
        self.__read_only = read_only
        self.bounds: List[Tuple[int, int]] = []
        if filled_arr is not None:
            self.bounds = []
            for i in filled_arr.shape:
                self.bounds.append((1, i))

            self._reset()
            for idx, val in np.ndenumerate(filled_arr):
                one_indexed = cast(IndexT, tuple(map(lambda x: x + 1, idx)))
                # use native Python types for the values
                self.entries[one_indexed] = val.item()

    def diff(self, other: ArbitraryIndexArray[IndexT]) -> DiffDescription:
        """
        Returns a dictionary with description of differences between this and the given ArbitraryIndexArray.
        """
        same_bounds = True
        uninitialized: List[IndexT] = []
        first_wrong_val = None

        if self.bounds != other.bounds:
            same_bounds = False

        for i in other.entries:
            if i not in self.entries:
                uninitialized.append(i)
            elif self.entries[i] != other.entries[i] and first_wrong_val is None:
                first_wrong_val = i

        return DiffDescription(
            same_bounds=same_bounds,
            uninitialized=uninitialized,
            first_wrong_val=first_wrong_val,
        )

    def is_read_only(self) -> bool:
        return self.__read_only

    def _reset(self) -> None:
        self.entries: OrderedDict[IndexT, ElementT] = OrderedDict()

    def set_bounds(self, *args: Tuple[int, int]) -> None:
        if self.__read_only:
            raise DPCodingException("Bounds cannot be changed in a read-only array.")
        self.bounds = []
        for bound in args:
            if not isinstance(bound, tuple):
                raise DPCodingException("Bounds must be given as tuples.")
            self.bounds.append(bound)
        self._reset()

    def __getitem__(self, idx: InputIdxT) -> ElementT:
        idx_tuple = self._to_tuple(idx)
        self._check_bounds(idx_tuple)
        if idx_tuple not in self.entries:
            idx_str = ", ".join(map(str, idx_tuple))
            raise DPCodingException(
                f"Your code tried to access {self.name}[{idx_str}], but this has not yet been evaluated yet."
            )
        return self.entries[idx_tuple]

    def __setitem__(self, idx: InputIdxT, val: ElementT) -> None:
        if self.__read_only:
            raise DPCodingException(f"The array {self.name} is set as read only.")
        idx_tuple = self._to_tuple(idx)
        self._check_bounds(idx_tuple)
        self.entries[idx_tuple] = val

    def _check_bounds(self, idx: IndexT) -> None:
        if self.bounds is None or len(self.bounds) == 0:
            raise DPCodingException("You must first set the bounds of the array.")

        if len(idx) != len(self.bounds):
            idx_str = idx if isinstance(idx, int) else ", ".join(map(str, idx))
            raise DPCodingException(
                f"Your code attempted to access {self.name}[{idx_str}], but {self.name} is {len(self.bounds)}-D."
            )

        # check if idx within bounds
        for i in range(len(idx)):
            if idx[i] < self.bounds[i][0] or idx[i] > self.bounds[i][1]:
                idx_str = idx if isinstance(idx, int) else ", ".join(map(str, idx))
                raise DPCodingException(
                    f"Your code attempted to access {self.name}[{idx_str}], but you set your array bounds as {self.name}{self.bounds}."
                )

    def _to_tuple(self, idx: InputIdxT) -> IndexT:
        if isinstance(idx, tuple):
            return cast(IndexT, idx)
        elif isinstance(idx, int):
            return cast(IndexT, (idx,))

        assert_never(idx)
