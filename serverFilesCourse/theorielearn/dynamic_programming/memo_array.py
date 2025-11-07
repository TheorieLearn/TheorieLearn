from math import nan
from typing import List, Optional

import numpy as np

from theorielearn.dynamic_programming.arbitrary_index_array import (
    ArbitraryIndexArray,
    ElementT,
    IndexT,
    InputIdxT,
)
from theorielearn.dynamic_programming.dp_coding_exception import DPCodingException


class MemoArray(ArbitraryIndexArray[IndexT]):
    """
    Represents a memoization array for guided dynamic programming problems
    """

    def __init__(self, filled_arr: Optional[np.ndarray] = None, name: str = "") -> None:
        super().__init__(filled_arr=filled_arr, name=name)
        self.__read_only = False

    def _reset(self) -> None:
        super()._reset()
        # indices of past invalid accesses for feedback output
        self.__invalid_accesses: List[str] = []
        self.__last_get_invalid: bool = False

    def __getitem__(self, idx: InputIdxT) -> ElementT:
        idx_tuple = self._to_tuple(idx)
        self._check_bounds(idx_tuple)
        if idx_tuple not in self.entries:
            idx_str = ", ".join(map(str, idx_tuple))
            self.__invalid_accesses.append(f"{self.name}[{idx_str}]")
            self.__last_get_invalid = True
            return nan
        return self.entries[idx_tuple]

    def __setitem__(self, idx: InputIdxT, val: ElementT) -> None:
        idx_tuple = self._to_tuple(idx)
        self._check_bounds(idx_tuple)
        if self.__last_get_invalid:
            # Reset invalid access list for next mistake
            idx_str = ", ".join(map(str, idx_tuple))
            invalid_accesses = self.__invalid_accesses
            self.__invalid_accesses = []
            self.__last_get_invalid = False
            raise DPCodingException(
                f"When evaluating {self.name}[{idx_str}], your code tried to access the following uninitialized entries: {invalid_accesses}"
            )
        self.entries[idx_tuple] = val
