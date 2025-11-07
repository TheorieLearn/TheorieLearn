from __future__ import annotations

import bisect
import copy
import math
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Generic, Optional, TypeVar

from typing_extensions import Protocol


def identity(x: Any) -> Any:
    return x


# This class was taken from here:
# https://stackoverflow.com/questions/47965083/comparable-types-with-mypy
# Should function as a generic type but allow comparison operators to still be used
C = TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __lt__(self: C, other: C) -> bool:
        pass

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


T = TypeVar("T", bound=Comparable)


# Constructor defaults to an empty value list, btree_insert is built to handle this case so it is okay to initialize without any values
@dataclass
class BtreeNode(Generic[T]):
    values: list[T] = field(default_factory=list)
    children: list[BtreeNode[T]] = field(default_factory=list)
    m: int = 3

    # simply compares values in the node and then insures all children are equal, recursively.
    # Does not explicity check 'm'
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BtreeNode):
            return NotImplemented
        if len(self.values) != len(other.values) or len(self.children) != len(
            other.children
        ):
            return False
        for a, b in zip(self.values, other.values):
            if a != b:
                return False
        for childa, childb in zip(self.children, other.children):
            if childa != childb:
                return False
        return True

    # For debugging
    def printTree(self):
        print(self.values)
        for c in self.children:
            c.printTree()

    # If tie, insert after existing elements.
    # promote - prefer to promote right
    # Inserts value into btree according to current btree rules
    # Returns new root node. This may be different than before so variables need to be redefined
    # i.e. b = b.btree_insert(val)
    def btree_insert(self, value: T) -> BtreeNode[T]:
        """
        Inserts value into btree.
        Return the new root, which may be a new value. Use syntax root = root.btree_insert(val)
        If there are two 'middle' nodes when promotion occurs, promotes the right one
        """
        if self.m < 3:
            raise ValueError("BtreeNode must have m of at least 3")
        childret = self._btree_insert_rec(value)
        if childret[1] is not None and childret[2] is not None:
            newRoot = BtreeNode(
                values=[childret[2]], children=[childret[0], childret[1]], m=self.m
            )
            return newRoot
        else:
            return self

    # return (node1, -node2, -value)
    # internal portion of btree inserting.
    # after a node has been inserted into, it returns [current node, None, None] so the parent can be updated.
    # If a promotion is required, it returns [left child, right child, promotion value]
    # so the parent can accept the new value and assign children
    # recursively promotes every step necessary
    def _btree_insert_rec(
        self, value: T
    ) -> tuple[BtreeNode[T], Optional[BtreeNode[T]], Optional[T]]:
        if len(self.values) == 0:
            self.values = [value]
            return (self, None, None)
        if len(self.children) == 0:
            bisect.insort_right(self.values, value)
        else:
            childind = bisect.bisect_right(self.values, value)
            childret = self.children[childind]._btree_insert_rec(value)
            if childret[1] is not None and childret[2] is not None:
                self.values.insert(childind, childret[2])
                self.children[childind] = childret[0]
                self.children.insert(childind + 1, childret[1])
            else:
                self.children[childind] = childret[0]
        if len(self.values) == self.m:
            promoteInd = math.floor(len(self.values) / 2)
            promoteVal = self.values[promoteInd]
            rightNode = BtreeNode(
                values=self.values[(promoteInd + 1) :],
                children=self.children[(promoteInd + 1) :],
                m=self.m,
            )
            self.values = self.values[:promoteInd]
            self.children = self.children[: promoteInd + 1]
            return (self, rightNode, promoteVal)
        else:
            return (self, None, None)

    # Doesn't make a deep copy. Should only be used in recursive calls so btree doesn't make n deepcopies of O(n) trees
    def _to_dict(self) -> dict[str, Any]:
        return {
            "value": self.values,
            "children": [child.to_dict() for child in self.children],
        }

    # Makes a deep copy and converts to dict. External code should always call this version to prevent messing with code after
    # converting to dict.
    def to_dict(self) -> dict[str, Any]:
        cop = copy.deepcopy(self)
        return {
            "value": cop.values,
            "children": [child._to_dict() for child in cop.children],
        }

    # If this is used by the grader, it will catch errors and display them to the student, so we send extra errors when grader=True
    # Converts a dictionary to a btreenode object.
    @staticmethod
    def from_dict(
        dict_: dict[str, Any],
        cast_func: Callable[[Any], T] = identity,
        grader: bool = False,
    ) -> BtreeNode[T]:
        value = dict_["value"]
        if grader:
            for v in value:
                if v == "":
                    raise ValueError("Tree Nodes should not be left without a value.")
        try:
            value = [cast_func(val) for val in value]
        except ValueError:
            raise ValueError(
                f'Cannot represent element in "{value}" as {cast_func.__name__}.'
            )

        rawchildren = dict_["children"]
        node = BtreeNode(
            value,
            [BtreeNode.from_dict(child, cast_func, grader) for child in rawchildren],
        )
        return node

    # Return a list of every value of the Btree in the order they should be sorted
    def _all_values(self) -> list[T]:
        if len(self.children) == 0:
            return self.values
        else:
            vals = []
            for c, v in zip(self.children, self.values):
                vals += c._all_values()
                vals.append(v)
            vals += self.children[-1]._all_values()
            return vals

    # Makes sure the btree is properly sorted
    def valid_btree_sort(self) -> bool:
        student_vals = self._all_values()
        return student_vals == sorted(student_vals)

    # Determines if the tree is a valid m-ary btree
    def _check_m(self, m: int, root: bool = True) -> bool:
        if not root and (
            len(self.values) >= m or len(self.values) < math.ceil(m / 2) - 1
        ):
            return False
        for c in self.children:
            if not c._check_m(m, False):
                return False
        return True

    def min_max_m(self) -> tuple[int, int]:
        """
        Returns the minimum and maximum possible values of m for the given tree.
        """
        m = 1
        min = 0
        max = 0
        while min == 0 or max == 0:
            m += 1  # 2 is minimum
            valid = self._check_m(m)
            if valid and min == 0:
                min = m
            if not valid and min != 0:
                max = m - 1

        return min, max

    # Counts how many 'disk seeks' required to find a specific value in a btree (root = 1)
    def count_seeks(self, value: T) -> int:
        if value in self.values:
            return 1
        if len(self.children) == 0:
            raise ValueError("Value not in btree")
        for i, v in enumerate(self.values):
            if value < v:
                return 1 + self.children[i].count_seeks(value)
        return 1 + self.children[-1].count_seeks(value)

    # for two non equal btrees, report the first element that isn't equal.
    # Reports the val from the first tree (student) instead of correct tree
    # assumes they aren't equal and have the same number of elements.
    def _val_report_eq_(self, other: BtreeNode[T]) -> Optional[T]:
        for a, b in zip(self.values, other.values):
            if a != b:
                return a
        for childa, childb in zip(self.children, other.children):
            bad_val = childa._val_report_eq_(childb)
            if bad_val is not None:
                return bad_val
        return None

    # Function that returns the grader function once called (not the grader itself)
    # ref_dict -> The correct tree. should be a BtreeNode object that has had .to_dict() called on it
    # cast_func -> transforms the type from the submitted element json (string) to the type used in the grading tree. typically 'int'
    # extra_feedback -> More specific in why the problem is wrong. Can give hints for not sorting the tree by btree rules,
    # having to many values in a node for the m property, or if the btree is valid but doesn't match the correct answer.
    # valid_sort_weight -> the portion of the score that should come from sorting by btree rules.
    # valid_m_weight -> The portion of the score that comes from understanding the 'm' property and
    # valid sort and valid m now depend on the tree having the correct number of elements (not necessarily the correct number of nodes)
    # not putting too many elements in a node (note, a single element will win this)
    @staticmethod
    def tree_grader(
        ref_dict: dict[str, Any],
        cast_func: Callable[[Any], T] = identity,
        extra_feedback: bool = True,
        valid_sort_weight: float = 0.25,
        valid_m_weight: float = 0.25,
        report_first_bad_val: bool = True,
    ) -> Callable[[Any], tuple[float, str]]:
        ref_tree = BtreeNode.from_dict(ref_dict, cast_func)

        def inner_tree_grader(raw_student_sub: dict[str, Any]) -> tuple[float, str]:
            try:
                student_tree = BtreeNode.from_dict(
                    raw_student_sub, cast_func, grader=True
                )
            except ValueError as err:
                return 0.0, str(err)

            score = 0.0
            feedback = ""

            student_val_count = len(student_tree._all_values())
            ref_val_count = len(ref_tree._all_values())
            if student_val_count < ref_val_count:
                if extra_feedback:
                    feedback = f"The tree you built does not have enough elements. There should be {ref_val_count} values in your tree"
                else:
                    feedback = "The tree you built is not correct."
            elif ref_val_count < student_val_count:
                if extra_feedback:
                    feedback = f"The tree you built has too many elements. There should be {ref_val_count} values in your tree"
                else:
                    feedback = "The tree you built is not correct."
            else:
                if student_tree.valid_btree_sort():
                    score += valid_sort_weight
                else:
                    if extra_feedback:
                        feedback = "The tree you built is not properly sorted."
                    else:
                        feedback = "The tree you built is not correct."

                if student_tree._check_m(ref_tree.m):
                    score += valid_m_weight
                else:
                    if extra_feedback and feedback == "":
                        feedback = (
                            f"The tree you built is not a valid m={ref_tree.m} btree."
                        )
                    elif not extra_feedback:
                        "The tree you built is not correct."

                if student_tree == ref_tree:
                    score = 1.0
                    feedback = "Correct!"
                else:
                    if report_first_bad_val and feedback == "":
                        feedback = f"The values in this tree do not match the correct tree. {student_tree._val_report_eq_(ref_tree)} is the first incorrect value."
                    elif extra_feedback and feedback == "":
                        feedback = f"This is a valid m={ref_tree.m} btree but it does not match the solution."
                    elif not extra_feedback:
                        feedback = "The tree you built is not correct."

            return score, feedback

        return inner_tree_grader
