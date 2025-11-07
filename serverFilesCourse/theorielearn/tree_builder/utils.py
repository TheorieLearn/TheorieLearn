from __future__ import annotations

import copy
import math
import random
from abc import abstractmethod
from collections import deque
from dataclasses import dataclass
from enum import Enum
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


@dataclass
class TreeBuilderNode(Generic[T]):
    value: T
    left: Optional[TreeBuilderNode[T]]
    right: Optional[TreeBuilderNode[T]]
    highlight: bool = False
    subtree: bool = False
    height: int = 0  # In general, this value is NOT MAINTAINED. It is routinely updated in AVL trees.
    # Otherwise, don't assume you can access height without explicitly calling something to update it. (e.g. set_tree_height())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TreeBuilderNode):
            return NotImplemented

        stack: deque = deque()
        stack.append((self, other))
        while len(stack) > 0:
            s, o = stack.pop()
            if s is None and o is None:
                continue
            elif s is None or o is None:
                return False
            else:
                if s.value != o.value or s.subtree != o.subtree:
                    return False
                stack.append((s.left, o.left))
                stack.append((s.right, o.right))
        return True

    # Clear val will turn the tree into an empty one with the same values
    def to_dict(self, clear_val=False) -> dict[str, Any]:
        return {
            "value": "" if clear_val else self.value,
            "left": self.left.to_dict(clear_val) if self.left is not None else None,
            "right": self.right.to_dict(clear_val) if self.right is not None else None,
            "highlight": self.highlight,
            "subtree": self.subtree,
        }

    # Generates a BST with count unique node values, all integers ranging from minVal to maxVal.
    # If maxVal is ommitted or set low, it is adjusted to ensure at least count unique values.
    @staticmethod
    def gen_random_tree(
        count: int, maxVal: int = 0, minVal: int = 1
    ) -> TreeBuilderNode:
        root, _ = TreeBuilderNode.gen_random_tree_with_list(count, maxVal, minVal)
        return root

    @staticmethod
    def gen_random_tree_with_list(
        count: int, maxVal: int = 0, minVal: int = 1
    ) -> tuple[TreeBuilderNode, list[int]]:
        if maxVal - minVal - 1 < count:
            maxVal = minVal + 1 + count
        sequence = random.sample(range(minVal, maxVal), count)
        iterator = iter(sequence)
        root: TreeBuilderNode = TreeBuilderNode(next(iterator), None, None)
        for v in iterator:
            root.insert_random(v)
        return root, sequence

    def insert_random(self, value: T):
        if random.random() < 0.5:
            if self.left is None:
                self.left = TreeBuilderNode(value, None, None)
            else:
                self.left.insert_random(value)
        else:
            if self.right is None:
                self.right = TreeBuilderNode(value, None, None)
            else:
                self.right.insert_random(value)

    def _calculate_size(self) -> int:
        size = 0
        stack: deque = deque()
        stack.append(self)
        while len(stack) > 0:
            node = stack.pop()
            size += 1
            if node.left is not None:
                stack.append(node.left)
            if node.right is not None:
                stack.append(node.right)
        return size

    # Given a number of children ()
    def nodes_with_child_count(self, count: int) -> list[T]:
        if count not in [0, 1, 2]:
            raise ValueError("Binary Trees can only have 0, 1, or 2 children")
        if self.left is not None and self.right is not None:
            childret = self.right.nodes_with_child_count(
                count
            ) + self.left.nodes_with_child_count(count)
            if count == 2:
                return [self.value] + childret
            else:
                return childret
        elif self.right is not None:
            childret = self.right.nodes_with_child_count(count)
            if count == 1:
                return [self.value] + childret
            else:
                return childret
        elif self.left is not None:
            childret = self.left.nodes_with_child_count(count)
            if count == 1:
                return [self.value] + childret
            else:
                return childret
        else:
            if count == 0:
                return [self.value]
            else:
                return []

    @staticmethod
    def is_perfect(node: Optional[TreeBuilderNode[T]], height: int) -> bool:
        if height < -1:
            return False
        if height == -1 and node is None:
            return True
        elif node is None:
            return False
        else:
            return TreeBuilderNode.is_perfect(
                node.left, height - 1
            ) and TreeBuilderNode.is_perfect(node.right, height - 1)

    @staticmethod
    def is_complete(node: Optional[TreeBuilderNode[T]], height: int) -> bool:
        if height == -1 and node is None:
            return True
        elif node is None:
            return False
        else:
            return (
                TreeBuilderNode.is_complete(node.left, height - 1)
                and TreeBuilderNode.is_perfect(node.right, height - 2)
                or (
                    TreeBuilderNode.is_perfect(node.left, height - 1)
                    and TreeBuilderNode.is_complete(node.right, height - 1)
                )
            )

    @staticmethod
    def is_full(node: TreeBuilderNode[T]) -> bool:
        if node.left is None and node.right is None:
            return True
        elif node.left is None or node.right is None:
            return False
        else:
            return TreeBuilderNode.is_full(node.left) and TreeBuilderNode.is_full(
                node.right
            )

    @staticmethod
    def calc_tree_height(node: Optional[TreeBuilderNode[T]]) -> int:
        if node is None:
            return -1
        return 1 + max(
            TreeBuilderNode.calc_tree_height(node.left),
            TreeBuilderNode.calc_tree_height(node.right),
        )

    def is_tree_balanced(self) -> bool:
        self.set_tree_height()
        rh = -1 if self.right is None else self.right.height
        lh = -1 if self.left is None else self.left.height
        if abs(rh - lh) >= 2:
            return False
        else:
            return (self.right is None or self.right.is_tree_balanced()) and (
                self.left is None or self.left.is_tree_balanced()
            )

    # Sets the "height" attribute for every node of the tree
    def set_tree_height(self) -> int:
        left_height = -1 if self.left is None else self.left.set_tree_height()
        right_height = -1 if self.right is None else self.right.set_tree_height()
        self.height = 1 + max(left_height, right_height)
        return self.height

    # Returns a new tree, of the same shape, where each node's value is the height at that node.
    # Assumes set_tree_height has already been called
    def get_height_tree(self) -> TreeBuilderNode:
        return TreeBuilderNode(
            self.height,
            None if self.left is None else self.left.get_height_tree(),
            None if self.right is None else self.right.get_height_tree(),
        )

    # returns a new tree matching the same structure, with the values matching the designated "order".
    # order is either "pre" "post" "in" or "level"
    # defaults to zero-indexed, unless first_index is changed
    def get_traversal_tree(self, order: str, first_index: int = 0) -> TreeBuilderNode:
        if order == "pre":
            return (self._preorder_traversal_tree(first_index))[0]
        elif order == "in":
            return (self._inorder_traversal_tree(first_index))[0]
        elif order == "post":
            return (self._postorder_traversal_tree(first_index))[0]
        else:  # order == 'level'
            ret: list[Optional[TreeBuilderNode]] = (
                TreeBuilderNode._levelorder_traversal_tree([self], first_index)
            )
            return (
                TreeBuilderNode(first_index, None, None) if ret[0] is None else ret[0]
            )

    # returns a list of the trees values in the order they will be visitied.
    # order can be "pre" "post" "in" or "level"
    def get_traversal_list(self, order: str) -> list[T]:
        keytree = self.get_traversal_tree(order)
        orderdict = TreeBuilderNode._match_trees_to_dict(keytree, self)
        return [item for i, item in sorted(orderdict.items())]

    # Assumes correct length and no repetition
    def is_valid_levelorder(self, traversal: list[T]) -> bool:
        levels = TreeBuilderNode._get_tree_levels([self])
        start = 0
        for i, level in sorted(levels.items()):
            trav_level = traversal[start : start + len(level)]
            for element in level:
                if element not in trav_level:
                    return False
            start += len(level)
        return True

    def _preorder_traversal_tree(self, current: int = 0) -> tuple[TreeBuilderNode, int]:
        leftTree, rightval = (
            self.left._preorder_traversal_tree(current + 1)
            if self.left is not None
            else (None, current + 1)
        )
        rightTree, endval = (
            self.right._preorder_traversal_tree(rightval)
            if self.right is not None
            else (None, rightval)
        )
        root = TreeBuilderNode(current, leftTree, rightTree)
        return root, endval

    def _inorder_traversal_tree(self, current: int = 0) -> tuple[TreeBuilderNode, int]:
        leftTree, rightval = (
            self.left._inorder_traversal_tree(current)
            if self.left is not None
            else (None, current)
        )
        rightTree, endval = (
            self.right._inorder_traversal_tree(rightval + 1)
            if self.right is not None
            else (None, rightval + 1)
        )
        root = TreeBuilderNode(rightval, leftTree, rightTree)
        return root, endval

    def _postorder_traversal_tree(
        self, current: int = 0
    ) -> tuple[TreeBuilderNode, int]:
        leftTree, rightval = (
            self.left._postorder_traversal_tree(current)
            if self.left is not None
            else (None, current)
        )
        rightTree, endval = (
            self.right._postorder_traversal_tree(rightval)
            if self.right is not None
            else (None, rightval)
        )
        root = TreeBuilderNode(endval, leftTree, rightTree)
        return root, endval + 1

    # This non-intuitive way of doing the traversal partially owes to the fact that mypy won't
    # let me edit in place (can't confirm T is int).
    # Takes in a list of nodes (representing a level) and returns a list of Nodes (that level with the new values & children).
    # Any "holes" in a level are represent by None.
    @staticmethod
    def _levelorder_traversal_tree(
        nodes: list[Optional[TreeBuilderNode]], next: int = 0
    ) -> list[Optional[TreeBuilderNode]]:
        values: list[Optional[int]] = [
            (next := next + 1) - 1 if node is not None else None for node in nodes
        ]
        children: list[Optional[TreeBuilderNode]] = []
        has_children = False
        for node in nodes:
            if node is None:
                children.append(None)
                children.append(None)
            else:
                has_children = True
                children.append(node.left)
                children.append(node.right)
        child_trees = (
            children
            if not has_children
            else TreeBuilderNode._levelorder_traversal_tree(children, next)
        )

        new_trees: list[Optional[TreeBuilderNode]] = []
        for i, value in enumerate(values):
            if value is None:
                new_trees.append(None)
            else:
                new_trees.append(
                    TreeBuilderNode(value, child_trees[i * 2], child_trees[i * 2 + 1])
                )

        return new_trees

    @staticmethod
    def _get_tree_levels(
        levelnodes: list[TreeBuilderNode[T]], level: int = 0
    ) -> dict[int, list[T]]:
        if len(levelnodes) == 0:
            return dict()
        childlevel = []
        for node in levelnodes:
            if node.left is not None:
                childlevel.append(node.left)
            if node.right is not None:
                childlevel.append(node.right)
        childdict = TreeBuilderNode._get_tree_levels(childlevel, level + 1)
        childdict[level] = [n.value for n in levelnodes]
        return childdict

    # returns a dict of the values of keytree -> the values of valuetree
    # assumes the trees ahve the same shape
    @staticmethod
    def _match_trees_to_dict(
        keytree: Optional[TreeBuilderNode], valuetree: Optional[TreeBuilderNode]
    ) -> dict[Any, Any]:
        if keytree is None or valuetree is None:
            return dict()
        left = TreeBuilderNode._match_trees_to_dict(keytree.left, valuetree.left)
        right = TreeBuilderNode._match_trees_to_dict(keytree.right, valuetree.right)
        left.update(right)
        left[keytree.value] = valuetree.value
        return left

    # Returns new tree of same shape where the values in each node are the balances of the node
    def get_balance_tree(self) -> TreeBuilderNode:
        self.set_tree_height()
        return self._get_balance_tree_subfunc()

    # The recursive worker function for get_balance_tree
    def _get_balance_tree_subfunc(self) -> TreeBuilderNode:
        balance = (-1 if self.right is None else self.right.height) - (
            -1 if self.left is None else self.left.height
        )
        return TreeBuilderNode(
            balance,
            None if self.left is None else self.left._get_balance_tree_subfunc(),
            None if self.right is None else self.right._get_balance_tree_subfunc(),
            self.highlight,
            self.subtree,
            self.height,
        )

    def _get_zero_tree(self) -> TreeBuilderNode:
        return TreeBuilderNode(
            0,
            None if self.left is None else self.left._get_zero_tree(),
            None if self.right is None else self.right._get_zero_tree(),
            self.highlight,
            self.subtree,
        )

    def get_node_neighbors(self, value: T) -> tuple[bool, list[T]]:
        if self.value == value:
            out = []
            if self.right is not None:
                out.append(self.right.value)
            if self.left is not None:
                out.append(self.left.value)
            return True, out
        if self.left is None and self.right is None:
            return False, []
        if self.left is not None:
            b, l = self.left.get_node_neighbors(value)
            if b:
                if self.left.value == value:
                    l.append(self.value)
                return b, l
        if self.right is not None:
            b, l = self.right.get_node_neighbors(value)
            if b:
                if self.right.value == value:
                    l.append(self.value)
                return b, l
        return False, []

    def get_node_descendants(self, value: T, found=False) -> list[T]:
        add = [self.value] if found else []
        found = found or self.value == value
        return (
            add
            + (
                self.left.get_node_descendants(value, found)
                if self.left is not None
                else []
            )
            + (
                self.right.get_node_descendants(value, found)
                if self.right is not None
                else []
            )
        )

    def get_node_ancestors(self, value: T) -> tuple[list[T], bool]:
        if self.value == value:
            return [], True
        if self.left is not None:
            la, ls = self.left.get_node_ancestors(value)
            if ls:
                la.append(self.value)
                return la, True
        if self.right is not None:
            ra, rs = self.right.get_node_ancestors(value)
            if rs:
                ra.append(self.value)
                return ra, True
        return [], False

    def get_leaves_internals(self, is_root: bool = True) -> tuple[list[T], list[T]]:
        if self.left is None and self.right is None:
            return [self.value], []
        internals = [] if is_root else [self.value]
        leaves = []
        if self.right is not None:
            l, i = self.right.get_leaves_internals(False)
            internals += i
            leaves += l
        if self.left is not None:
            l, i = self.left.get_leaves_internals(False)
            internals += i
            leaves += l
        return leaves, internals

    def get_random_leaf(self) -> T:
        if self.left is not None and self.right is not None:
            if random.random() < 0.5:
                return self.left.get_random_leaf()
            else:
                return self.right.get_random_leaf()
        elif self.left is not None:
            return self.left.get_random_leaf()
        elif self.right is not None:
            return self.right.get_random_leaf()
        else:
            return self.value

    class DefGrade(str, Enum):
        Required = "Required"
        Forbidden = "Forbidden"
        Ignored = "Ignored"

    # This is for grading the questions of the type 'Build a tree of height 3 that is a full tree but not a perfect tree'
    @staticmethod
    def category_tree_grader(
        height: int,
        perfect: DefGrade,
        complete: DefGrade,
        full: DefGrade,
        reduce_feedback: bool = False,
    ) -> Callable[[Any], tuple[float, str]]:
        req, forb = (
            TreeBuilderNode.DefGrade.Required,
            TreeBuilderNode.DefGrade.Forbidden,
        )

        if perfect == req and (full == forb or complete == forb):
            raise ValueError(
                "The combination of inputs for perfect, complete, full is impossible"
            )

        def inner_tree_grader(raw_student_sub: dict[str, Any]) -> tuple[float, str]:
            try:
                student_tree: TreeBuilderNode = TreeBuilderNode.from_dict(
                    raw_student_sub
                )
            except ValueError as err:
                return 0.0, str(err)

            score = 0.0
            feedback = ""
            isperfect = TreeBuilderNode.is_perfect(student_tree, height)
            iscomplete = TreeBuilderNode.is_complete(student_tree, height)
            isfull = TreeBuilderNode.is_full(student_tree)
            if TreeBuilderNode.calc_tree_height(student_tree) != height:
                if reduce_feedback:
                    feedback = "The tree you built does not meet the given requirements"
                else:
                    feedback = "The tree you built does not have the correct height"
            elif perfect == req and not isperfect:
                if reduce_feedback:
                    feedback = "The tree you built does not meet the given requirements"
                else:
                    feedback = "The tree you built is not a perfect tree"
            elif perfect == forb and isperfect:
                if reduce_feedback:
                    feedback = "The tree you built does not meet the given requirements"
                else:
                    feedback = "The tree you built is a perfect tree"
            elif full == req and not isfull:
                if reduce_feedback:
                    feedback = "The tree you built does not meet the given requirements"
                else:
                    feedback = "The tree you built is not a full tree"
            elif full == forb and isfull:
                if reduce_feedback:
                    feedback = "The tree you built does not meet the given requirements"
                else:
                    feedback = "The tree you built is a full tree"
            elif complete == req and not iscomplete:
                if reduce_feedback:
                    feedback = "The tree you built does not meet the given requirements"
                else:
                    feedback = "The tree you built is not a complete tree"
            elif complete == forb and iscomplete:
                if reduce_feedback:
                    feedback = "The tree you built does not meet the given requirements"
                else:
                    feedback = "The tree you built is a complete tree"
            else:
                feedback = "Correct!"
                score = 1.0

            return score, feedback

        return inner_tree_grader

    @staticmethod
    def partial_tree_equality(
        ref_tree: TreeBuilderNode, comp_tree: TreeBuilderNode
    ) -> float:
        if ref_tree is None or comp_tree is None:
            return 0
        stack: deque = deque()
        stack.append((ref_tree, comp_tree))
        correct_nodes = 0
        while len(stack) > 0:
            ref, comp = stack.pop()
            if ref.value == comp.value and ref.subtree == comp.subtree:
                correct_nodes += 1
                # If one is none but the other isn't, it's wrong. If there both none, nothing to check
                if ref.left is not None and comp.left is not None:
                    stack.append((ref.left, comp.left))
                if ref.right is not None and comp.right is not None:
                    stack.append((ref.right, comp.right))

        return min(
            correct_nodes / ref_tree._calculate_size(),
            correct_nodes / comp_tree._calculate_size(),
        )

    @staticmethod
    def tree_grader(
        ref_dict: dict[str, Any],
        cast_func: Callable[[Any], T] = identity,
        partial_credit: bool = False,
        default_tree_val: Optional[T] = None,
    ) -> Callable[[Any], tuple[float, str]]:
        ref_tree = TreeBuilderNode.from_dict(ref_dict, cast_func)

        def inner_tree_grader(raw_student_sub: dict[str, Any]) -> tuple[float, str]:
            try:
                student_tree = TreeBuilderNode.from_dict(
                    raw_student_sub,
                    cast_func,
                    grader=True,
                    default_value=default_tree_val,
                )
            except ValueError as err:
                return 0.0, str(err)

            score = 0.0
            feedback = ""
            if not partial_credit:
                if student_tree == ref_tree:
                    score = 1.0
                    feedback = "Correct!"
                else:
                    feedback = "The tree you built is not correct."
            else:
                score = TreeBuilderNode.partial_tree_equality(ref_tree, student_tree)
                if math.isclose(score, 1.0):
                    feedback = "Correct!"
                elif score == 0.0:
                    feedback = "The tree you built is not correct."
                else:
                    feedback = "The tree you built is partially correct."

            return score, feedback

        return inner_tree_grader

    # 3 Initiailization Methods at the end for sorting
    # They repeat for each subclass to assert the input matches the proposed type
    @staticmethod
    def from_dict(
        dict_: dict[str, Any],
        cast_func: Callable[[Any], T] = identity,
        grader: bool = False,
        default_value: Optional[T] = None,
    ) -> TreeBuilderNode[T]:
        value = dict_["value"]
        if default_value is not None and value == "":
            value = default_value
        elif grader and value == "":
            raise ValueError("Tree Nodes should not be left without a value.")
        try:
            value = cast_func(value)
        except ValueError:
            raise ValueError(f'Cannot represent "{value}" as {cast_func.__name__}.')

        node = TreeBuilderNode(value, None, None)
        left_val = dict_.get("left")
        right_val = dict_.get("right")
        node.highlight = dict_.get("highlight", False)
        node.subtree = dict_.get("subtree", False)
        if left_val is not None:
            node.left = TreeBuilderNode.from_dict(
                left_val, cast_func, grader, default_value
            )
        if right_val is not None:
            node.right = TreeBuilderNode.from_dict(
                right_val, cast_func, grader, default_value
            )
        return node

    @staticmethod
    def from_tuple(
        tuple_: Optional[tuple], cast_func: Callable[[Any], T] = identity
    ) -> Optional[TreeBuilderNode[T]]:
        if tuple_ is None:
            return None

        val, left_tup, right_tup = tuple_
        return TreeBuilderNode(
            cast_func(val),
            TreeBuilderNode.from_tuple(left_tup, cast_func),
            TreeBuilderNode.from_tuple(right_tup, cast_func),
        )


@dataclass(eq=False)
class BSTBuilderNode(TreeBuilderNode[T]):
    value: T
    left: Optional[BSTBuilderNode[T]]
    right: Optional[BSTBuilderNode[T]]
    highlight: bool = False
    subtree: bool = False

    # Inserts a value into the tree, following the rules of a BST
    def bst_insert(
        self,
        value: T,
        highlight: bool = False,
        subtree: bool = False,
    ) -> None:
        node = self
        while True:
            assert node
            if value < node.value:
                if node.left is None:
                    node.left = BSTBuilderNode(value, None, None, highlight, subtree)
                    break
                else:
                    node = node.left
            elif value > node.value:
                if node.right is None:
                    node.right = BSTBuilderNode(value, None, None, highlight, subtree)
                    break
                else:
                    node = node.right

    def _bst_find_rec(
        self, value: T, zero_tree: TreeBuilderNode, label: int = 1
    ) -> TreeBuilderNode:
        current = self.value
        zero_tree.value = label
        if value < current and self.left is not None and zero_tree.left is not None:
            zero_tree.left = self.left._bst_find_rec(value, zero_tree.left, label + 1)
            return zero_tree
        elif value > current and self.right is not None and zero_tree.right is not None:
            zero_tree.right = self.right._bst_find_rec(
                value, zero_tree.right, label + 1
            )
            return zero_tree
        else:
            return zero_tree

    def bst_find_label_tree(self, value: T) -> TreeBuilderNode:
        zero = self._get_zero_tree()
        return self._bst_find_rec(value, zero)

    def bst_find_sequence(self, value: T) -> list[T]:
        visited = [self.value]
        if value < self.value and self.left is not None:
            visited += self.left.bst_find_sequence(value)
        elif value > self.value and self.right is not None:
            visited += self.right.bst_find_sequence(value)
        return visited

    def _single_dir_swap(self, right: bool, topval: T) -> T:
        if right and self.right is not None:
            retval = self.right._single_dir_swap(right, topval)
            return retval
        elif right:
            retval = self.value
            self.value = topval
            return retval
        elif not right and self.left is not None:
            retval = self.left._single_dir_swap(right, topval)
            return retval
        else:
            retval = self.value
            self.value = topval
            return retval

    def _IO_Swap(self, IOP: bool):
        if IOP and self.left is not None:
            self.value = self.left._single_dir_swap(True, self.value)
        elif not IOP and self.right is not None:
            self.value = self.right._single_dir_swap(False, self.value)

    # Since the root may be changed, must not modify in place but be called as
    # root = root.bst_remove(value)
    # If toRemove is not in the tree, returns itself and changes nothing
    # If IOP is true, swaps with IOP. if false, uses IOS
    def bst_remove(self, toRemove: T, IOP: bool) -> Optional[BSTBuilderNode[T]]:
        if toRemove < self.value:
            if self.left is not None:
                self.left = self.left.bst_remove(toRemove, IOP)
            return self
        elif toRemove > self.value:
            if self.right is not None:
                self.right = self.right.bst_remove(toRemove, IOP)
            return self
        else:
            if self.left is not None and self.right is not None:
                self._IO_Swap(IOP)
                if IOP:
                    self.left = self.left.bst_remove(toRemove, IOP)
                else:
                    self.right = self.right.bst_remove(toRemove, IOP)
                return self
            elif self.left is not None:
                return self.left
            elif self.right is not None:
                return self.right
            else:
                return None

    # Generates a BST with count unique node values, all integers ranging from minVal to maxVal.
    # If maxVal is ommitted or set low, it is adjusted to ensure at least count unique values.
    @staticmethod
    def genRandomBST(count: int, maxVal: int = 0, minVal: int = 1) -> BSTBuilderNode:
        root, _ = BSTBuilderNode.genRandomBSTWithList(count, maxVal, minVal)
        return root

    @staticmethod
    def genRandomBSTWithList(
        count: int, maxVal: int = 0, minVal: int = 1
    ) -> tuple[BSTBuilderNode, list[int]]:
        if maxVal - minVal - 1 < count:
            maxVal = minVal + 1 + count
        sequence = random.sample(range(minVal, maxVal), count)
        iterator = iter(sequence)
        root: BSTBuilderNode = BSTBuilderNode(next(iterator), None, None)
        for v in iterator:
            root.bst_insert(v)
        return root, sequence

    # Same as above, but also returns a value within the range that is not present in the tree
    @staticmethod
    def genRandomBSTBonusVal(
        count: int, maxVal: int = 0, minVal: int = 1
    ) -> tuple[BSTBuilderNode, int]:
        if maxVal - minVal - 1 < count + 1:
            maxVal = minVal + 2 + count
        sequence = random.sample(range(minVal, maxVal), count + 1)
        iterator = iter(sequence)
        root: BSTBuilderNode = BSTBuilderNode(next(iterator), None, None)
        val = next(iterator)
        for v in iterator:
            root.bst_insert(v)
        return root, val

    # For animation mode. Returns the tree, list of input elements, and
    # list where each element is a dict for the tree at each step.
    @staticmethod
    def genRandomBSTWithFrames(
        count: int, maxVal: int = 0, minVal: int = 1
    ) -> tuple[BSTBuilderNode, list[int], list[dict[str, Any]]]:
        if maxVal - minVal - 1 < count:
            maxVal = minVal + 1 + count
        sequence = random.sample(range(minVal, maxVal), count)
        iterator = iter(sequence)
        root: BSTBuilderNode = BSTBuilderNode(next(iterator), None, None)
        frames = [root.to_dict()]
        for v in iterator:
            root.bst_insert(v)
            frames.append(root.to_dict())
        return root, sequence, frames

    # Generates a BST with count unique node values, all integers ranging from minVal to maxVal.
    # If maxVal is ommitted or set low, it is adjusted to ensure at least count unique values.
    @staticmethod
    def _genRandomPartialBalanceBST(
        count: int, balanceCount: int, maxVal: int = 0, minVal: int = 1
    ) -> BSTBuilderNode:
        balanceCount = min(
            balanceCount, count - 1
        )  # make sure it's possible that this is unbalanced.
        if maxVal - minVal - 1 < count:
            maxVal = minVal + 1 + count
        sequence = random.sample(range(minVal, maxVal), count)
        iterator = iter(sequence)
        root: AVLBuilderNode = AVLBuilderNode(next(iterator), None, None)
        for _ in range(balanceCount):
            root = root.avl_insert(root, next(iterator))
        for v in iterator:
            root.bst_insert(v)
        return root

    # Brute force makes random BSTs until one of them is unbalanced
    # the first balanceCount inserts will receive AVL rotations, (to ensure the tree isn't obviously unbalanced)
    # All nodes after that won't.
    @staticmethod
    def genRandomUnbalancedBST(
        count: int, maxVal: int = 0, minVal: int = 1, balanceCount: int = 0
    ) -> BSTBuilderNode:
        if count < 3:
            raise ValueError(
                "Impossible for a tree with < 3 nodes to be unbalanced, this will never terminate"
            )
        tree = BSTBuilderNode._genRandomPartialBalanceBST(
            count, balanceCount, maxVal, minVal
        )
        while tree.is_tree_balanced():
            tree = BSTBuilderNode._genRandomPartialBalanceBST(
                count, balanceCount, maxVal, minVal
            )
        return tree

    # 3 Initiailization Methods at the end for sorting
    # They repeat for each subclass to assert the input matches the proposed type
    # These assert the input is a BST
    @staticmethod
    def from_dict_bst(
        dict_: dict[str, Any], cast_func: Callable[[Any], T] = identity
    ) -> BSTBuilderNode[T]:
        value = dict_["value"]
        try:
            value = cast_func(value)
        except ValueError:
            raise ValueError(f'Cannot represent "{value}" as {cast_func.__name__}')

        node = BSTBuilderNode(value, None, None)
        left_val = dict_.get("left")
        right_val = dict_.get("right")
        node.highlight = dict_.get("highlight", False)
        node.subtree = dict_.get("subtree", False)
        if left_val is not None:
            node.left = BSTBuilderNode.from_dict_bst(left_val, cast_func)
            if node.left.value > value:
                raise ValueError("The tree in this dict is not a BST")
        if right_val is not None:
            node.right = BSTBuilderNode.from_dict_bst(right_val, cast_func)
            if node.right.value < value:
                raise ValueError("The tree in this dict is not a BST")
        return node

    @staticmethod
    def from_tuple_bst(
        tuple_: Optional[tuple], cast_func: Callable[[Any], T] = identity
    ) -> Optional[BSTBuilderNode[T]]:
        if tuple_ is None:
            return None

        val, left_tup, right_tup = tuple_
        node = BSTBuilderNode(
            cast_func(val),
            BSTBuilderNode.from_tuple_bst(left_tup, cast_func),
            BSTBuilderNode.from_tuple_bst(right_tup, cast_func),
        )
        if node.left is not None and node.left.value > node.value:
            raise ValueError("The tree in this tuple is not a BST")
        if node.right is not None and node.right.value < node.value:
            raise ValueError("The tree in this tuple is not a BST")
        return node


@dataclass(eq=False)
class AVLBuilderNode(BSTBuilderNode[T]):
    value: T
    left: Optional[AVLBuilderNode[T]]
    right: Optional[AVLBuilderNode[T]]
    highlight: bool = False
    subtree: bool = False
    height: int = 0

    def _update_local_height(self) -> int:
        left_height = -1 if self.left is None else self.left.height
        right_height = -1 if self.right is None else self.right.height
        self.height = 1 + max(left_height, right_height)
        return self.height

    def _get_balance(self) -> int:
        left_height = -1 if self.left is None else self.left.height
        right_height = -1 if self.right is None else self.right.height
        return right_height - left_height

    # Rotations and AVL insert used https://favtutor.com/blogs/avl-tree-python
    # as a major reference but did not directly copy
    def rotate_right(self, node: AVLBuilderNode[T]) -> AVLBuilderNode[T]:
        assert node.left
        newroot = node.left
        temp = node.left.right
        # without the temp var
        newroot.right = node
        node.left = temp
        node._update_local_height()
        newroot._update_local_height()
        return newroot

    def rotate_left(self, node: AVLBuilderNode[T]) -> AVLBuilderNode[T]:
        assert node.right
        newroot = node.right
        temp = node.right.left
        newroot.left = node
        node.right = temp

        node._update_local_height()
        newroot._update_local_height()
        return newroot

    # If making an AVL tree, this must be used for all insertions
    # Also assumes all values are distinct. (Equal values are placed in the right subtree)
    # Returns the New Root
    def avl_insert(
        self,
        root: AVLBuilderNode[T],
        value: T,
        highlight: bool = False,
        subtree: bool = False,
    ) -> AVLBuilderNode[T]:
        if value < root.value:
            if root.left is None:
                root.left = AVLBuilderNode(value, None, None)
                root.left.highlight = highlight
                root.left.subtree = subtree
            else:
                root.left = self.avl_insert(root.left, value, highlight, subtree)
        else:
            if root.right is None:
                root.right = AVLBuilderNode(value, None, None)
                root.right.highlight = highlight
                root.right.subtree
            else:
                root.right = self.avl_insert(root.right, value, highlight, subtree)

        root._update_local_height()
        balance = root._get_balance()
        # left heavy
        if balance == -2:
            assert root.left
            lb = root.left._get_balance()
            if lb == -1:
                return self.rotate_right(root)
            else:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)
        elif balance == 2:
            assert root.right
            rb = root.right._get_balance()
            if rb == 1:
                return self.rotate_left(root)
            else:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

        return root

    # Modified version also returns a single string of "L", "R", LR", or "RL" to identify the rotation performed.
    def avl_insert_with_rotation(
        self,
        root: AVLBuilderNode[T],
        value: T,
        highlight: bool = False,
        subtree: bool = False,
    ) -> tuple[AVLBuilderNode[T], str]:
        rot = ""
        if value < root.value:
            if root.left is None:
                root.left = AVLBuilderNode(value, None, None)
                root.left.highlight = highlight
                root.left.subtree = subtree
            else:
                root.left, rot = self.avl_insert_with_rotation(
                    root.left, value, highlight, subtree
                )
        else:
            if root.right is None:
                root.right = AVLBuilderNode(value, None, None)
                root.right.highlight = highlight
                root.right.subtree
            else:
                root.right, rot = self.avl_insert_with_rotation(
                    root.right, value, highlight, subtree
                )

        root._update_local_height()
        balance = root._get_balance()
        # left heavy
        if balance == -2:
            assert root.left
            lb = root.left._get_balance()
            if lb == -1:
                return self.rotate_right(root), "R"
            else:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root), "LR"
        elif balance == 2:
            assert root.right
            rb = root.right._get_balance()
            if rb == 1:
                return self.rotate_left(root), "L"
            else:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root), "RL"

        return root, rot

    # Performs avl insert and rotation, returns tree as well as a "frame" (dict) of the tree at every
    # step for the animation. Does not store a frame of the initial tree state.
    def avl_insert_frames(
        self,
        root: AVLBuilderNode[T],
        value: T,
        highlight: bool = False,
        subtree: bool = False,
    ) -> tuple[AVLBuilderNode, list[dict[str, Any]]]:
        root, commands = self._avl_insert_with_rotation_command(
            root, value, highlight, subtree
        )
        frames = [root.to_dict()]
        for command in commands:
            root = self._complete_rotate_command(root, command)
            frames.append(root.to_dict())
        return root, frames

    # actually does the insertion, gives commands for rotations but doesn't do them
    def _avl_insert_with_rotation_command(
        self,
        root: AVLBuilderNode[T],
        value: T,
        highlight: bool = False,
        subtree: bool = False,
    ) -> tuple[AVLBuilderNode[T], list[tuple[str, T]]]:
        rot = []
        if value < root.value:
            if root.left is None:
                root.left = AVLBuilderNode(value, None, None)
                root.left.highlight = highlight
                root.left.subtree = subtree
            else:
                root.left, rota = self._avl_insert_with_rotation_command(
                    root.left, value, highlight, subtree
                )
                rot = rota
        else:
            if root.right is None:
                root.right = AVLBuilderNode(value, None, None)
                root.right.highlight = highlight
                root.right.subtree
            else:
                root.right, rota = self._avl_insert_with_rotation_command(
                    root.right, value, highlight, subtree
                )
                rot = rota
        # AVL trees are guaranteed to only rotate at one node on insert
        # since we don't actually do insert, it could trigger as unbalanced when
        # a rotation in children would have solved it
        if len(rot) > 0:
            return root, rot

        root._update_local_height()
        balance = root._get_balance()
        # left heavy
        if balance == -2:
            assert root.left
            lb = root.left._get_balance()
            if lb != -1:
                rot.append(("L", root.left.value))
            rot.append(("R", root.value))
        elif balance == 2:
            assert root.right
            rb = root.right._get_balance()
            if rb != 1:
                rot.append(("R", root.right.value))
            rot.append(("L", root.value))

        return root, rot

    # Does a BST find for command[1], then performs the rotation described by command[0] at that location
    # needed because in order to animate we need to save the full tree to a dict after each rotation
    def _complete_rotate_command(
        self, root: AVLBuilderNode[T], command: tuple[str, Optional[T]]
    ) -> AVLBuilderNode[T]:
        if command[1] is None or command[0] == "":
            return root
        if command[1] < root.value and root.left is not None:
            root.left = self._complete_rotate_command(root.left, command)
        elif command[1] > root.value and root.right is not None:
            root.right = self._complete_rotate_command(root.right, command)
        elif command[1] == root.value:
            if command[0] == "R":
                return self.rotate_right(root)
            elif command[0] == "L":
                return self.rotate_left(root)
        return root

    # Since the root may be changed, must not modify in place but be called as
    # root = root.bst_remove(value)
    # If toRemove is not in the tree, returns itself and changes nothing
    # If IOP is true, swaps with IOP. if false, uses IOS
    def avl_remove(
        self, root: AVLBuilderNode[T], toRemove: T, IOP: bool
    ) -> Optional[AVLBuilderNode]:
        return self.avl_remove_with_rotations(root, toRemove, IOP)[0]

    # Also returns list of all rotations completed
    def avl_remove_with_rotations(
        self, root: AVLBuilderNode[T], toRemove: T, IOP: bool
    ) -> tuple[Optional[AVLBuilderNode[T]], list[str]]:
        rotations: list[str] = []

        tree, rotations, _ = self._avl_remove_with_commands(root, toRemove, IOP)
        return tree, rotations

    # Also returns list of all rotations completed
    def _avl_remove_with_commands(
        self, root: AVLBuilderNode[T], toRemove: T, IOP: bool
    ) -> tuple[Optional[AVLBuilderNode[T]], list[str], list[tuple[str, T]]]:
        rotations: list[str] = []
        commands: list[tuple[str, T]] = []

        if toRemove < root.value:
            if root.left is not None:
                root.left, rotations, commands = self._avl_remove_with_commands(
                    root.left, toRemove, IOP
                )
        elif toRemove > root.value:
            if root.right is not None:
                root.right, rotations, commands = self._avl_remove_with_commands(
                    root.right, toRemove, IOP
                )
        else:
            if root.left is not None and root.right is not None:
                root._IO_Swap(IOP)
                if IOP:
                    root.left, rotations, commands = self._avl_remove_with_commands(
                        root.left, toRemove, IOP
                    )
                else:
                    root.right, rotations, commands = self._avl_remove_with_commands(
                        root.right, toRemove, IOP
                    )
            elif root.left is not None:
                root = root.left
            elif root.right is not None:
                root = root.right
            else:
                return None, [], []

        root._update_local_height()
        balance = root._get_balance()
        # print(f"Removing {toRemove}, Root = {root.value} {root.height} {balance}")
        # left heavy
        if balance == -2:
            assert root.left
            lb = root.left._get_balance()
            if lb == -1:
                rotations.append("R")
                commands.append(("R", root.value))
                return self.rotate_right(root), rotations, commands
            else:
                rotations.append("LR")
                commands.append(("L", root.left.value))
                commands.append(("R", root.value))
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root), rotations, commands
        elif balance == 2:
            assert root.right
            rb = root.right._get_balance()
            if rb == 1:
                rotations.append("L")
                commands.append(("L", root.value))
                return self.rotate_left(root), rotations, commands
            else:
                rotations.append("RL")
                commands.append(("R", root.right.value))
                commands.append(("L", root.value))
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root), rotations, commands

        return root, rotations, commands

    # only performs one action - either swaps with IOP/IOS, or deletes the node, not both
    # bool is true if it swapped, therefore another call is required
    def _avl_remove_single_frame(
        self, toRemove: T, IOP: bool, first: bool = True
    ) -> tuple[Optional[AVLBuilderNode], bool]:
        if toRemove < self.value:
            if self.left is not None:
                self.left, swap = self.left._avl_remove_single_frame(
                    toRemove, IOP, first
                )
                return self, swap
            return self, False
        elif toRemove > self.value:
            if self.right is not None:
                self.right, swap = self.right._avl_remove_single_frame(
                    toRemove, IOP, first
                )
                return self, swap
            return self, False
        else:
            if self.left is not None and self.right is not None:
                self._IO_Swap(IOP)
                if first:
                    return self, True
                if IOP:
                    self.left, _ = self.left._avl_remove_single_frame(
                        toRemove, IOP, first
                    )
                else:
                    self.right, _ = self.right._avl_remove_single_frame(
                        toRemove, IOP, first
                    )
                return self, False
            elif self.left is not None:
                return self.left, False
            elif self.right is not None:
                return self.right, False
            else:
                return None, False

    def avl_remove_frames(
        self, root: AVLBuilderNode[T], toRemove: T, IOP: bool
    ) -> tuple[AVLBuilderNode[T], list[dict[str, Any]]]:
        test_root = copy.deepcopy(root)
        test_root2 = copy.deepcopy(root)
        test_root3, _, commands = test_root._avl_remove_with_commands(
            test_root, toRemove, IOP
        )
        if test_root3 is not None:
            test_root = test_root3

        frames = []

        newroot, redo = root._avl_remove_single_frame(toRemove, IOP)
        if newroot is None:
            return root, []
        frames.append(newroot.to_dict())
        if redo:
            newroot, _ = test_root2._avl_remove_single_frame(toRemove, IOP, False)
            if newroot is not None:
                frames.append(newroot.to_dict())
        if newroot is not None:
            for command in commands:
                newroot = newroot._complete_rotate_command(newroot, command)
                frames.append(newroot.to_dict())
            root = newroot
        return root, frames

    # This is for the last element of the AVL question.
    # It deep copies the tree, and inserts as if its an AVL tree on one (for the solution)
    # and as if its a non-AVL BST on the other (for the question so the student has to perform the rotations)
    # Returns - Bool - True if the two trees are distinct
    # Node - the Solution tree
    # Node - The Question tree
    def AVL_BST_Copy_Insert(
        self, value: T, highlight: bool = False
    ) -> tuple[bool, AVLBuilderNode[T], BSTBuilderNode[T]]:
        QuestionTree: BSTBuilderNode[T] = copy.deepcopy(self)
        SolutionTree = self.avl_insert(self, value)
        QuestionTree.bst_insert(value, highlight)
        diff = not (SolutionTree == QuestionTree)
        return diff, SolutionTree, QuestionTree

    # 3 Initiailization Methods at the end for sorting
    # They repeat for each subclass to assert the input matches the proposed type
    # These assert the input is a AVL
    # Also auto-update height while building the tree
    @staticmethod
    def from_dict_avl(
        dict_: dict[str, Any], cast_func: Callable[[Any], T] = identity
    ) -> AVLBuilderNode[T]:
        value = dict_["value"]
        try:
            value = cast_func(value)
        except ValueError:
            raise ValueError(f'Cannot represent "{value}" as {cast_func.__name__}')

        node = AVLBuilderNode(value, None, None)
        left_val = dict_.get("left")
        right_val = dict_.get("right")
        node.highlight = dict_.get("highlight", False)
        node.subtree = dict_.get("subtree", False)
        if left_val is not None:
            node.left = AVLBuilderNode.from_dict_avl(left_val, cast_func)
            if node.left.value > value:
                raise ValueError("The tree in this dict is not a BST")
        if right_val is not None:
            node.right = AVLBuilderNode.from_dict_avl(right_val, cast_func)
            if node.right.value < value:
                raise ValueError("The tree in this dict is not a BST")

        node._update_local_height()
        balance = node._get_balance()
        if abs(balance) >= 2:
            raise ValueError(
                "The tree in this dict is not an AVL tree - it is unbalanced"
            )
        return node

    @staticmethod
    def from_tuple_avl(
        tuple_: Optional[tuple], cast_func: Callable[[Any], T] = identity
    ) -> Optional[AVLBuilderNode[T]]:
        if tuple_ is None:
            return None

        val, left_tup, right_tup = tuple_
        node = AVLBuilderNode(
            cast_func(val),
            AVLBuilderNode.from_tuple_avl(left_tup, cast_func),
            AVLBuilderNode.from_tuple_avl(right_tup, cast_func),
        )
        if node.left is not None and node.left.value > node.value:
            raise ValueError("The tree in this tuple is not a BST")
        if node.right is not None and node.right.value < node.value:
            raise ValueError("The tree in this tuple is not a BST")

        node._update_local_height()
        balance = node._get_balance()
        if abs(balance) >= 2:
            raise ValueError(
                "The tree in this tuple is not an AVL tree - it is unbalanced"
            )
        return node

    # Generates an AVL tree with count unique node values, all integers ranging from minVal to maxVal.
    # If maxVal is ommitted or set low, it is adjusted to ensure at least count unique values.
    @staticmethod
    def genRandomAVL(count: int, maxVal: int = 0, minVal: int = 1) -> AVLBuilderNode:
        return AVLBuilderNode.genRandomAVLWithList(count, maxVal, minVal)[0]

    @staticmethod
    def genRandomAVLWithList(
        count: int, maxVal: int = 0, minVal: int = 1
    ) -> tuple[AVLBuilderNode, list[int]]:
        if maxVal - minVal - 1 < count:
            maxVal = minVal + 1 + count
        sequence = random.sample(range(minVal, maxVal), count)
        iterator = iter(sequence)
        root: AVLBuilderNode = AVLBuilderNode(next(iterator), None, None)
        for v in iterator:
            root = root.avl_insert(root, v)
        return root, sequence

    @staticmethod
    def genRandomAVLWithFrames(
        count: int, maxVal: int = 0, minVal: int = 1
    ) -> tuple[AVLBuilderNode, list[int], list[dict[str, Any]]]:
        if maxVal - minVal - 1 < count:
            maxVal = minVal + 1 + count
        sequence = random.sample(range(minVal, maxVal), count)
        iterator = iter(sequence)
        root: AVLBuilderNode = AVLBuilderNode(next(iterator), None, None)
        frames = [root.to_dict()]
        for v in iterator:
            root, newFrames = root.avl_insert_frames(root, v)
            frames += newFrames
        return root, sequence, frames
