from __future__ import annotations

import re
from dataclasses import dataclass, field
from queue import Queue
from typing import Any, Callable, Generic, Optional, TypeVar, Union

import theorielearn.shared_utils as su
import sympy

T = TypeVar("T")


def identity(x: Any) -> Any:
    return x


# M-ary tree node to imply aribtrary child count, open to better name styling.
@dataclass
class MaryTreeNode(Generic[T]):
    value: Optional[T]
    children: list[MaryTreeNode] = field(default_factory=list)
    isSubtree: bool = False

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MaryTreeNode):
            return NotImplemented
        if self.value != other.value or len(self.children) != len(other.children):
            return False
        for childa, childb in zip(self.children, other.children):
            if childa != childb:
                return False
        return True

    # levels_to_check is not equivalent to the height, equivalent to how many rows to consider,
    # i.e. 1 compares only the root.
    # sympymode uses _sympy_equivalence() to compare values if true, otherwise just uses ==
    # assumes self is the reference and other is the student
    # Returns (correct, is other greater than self, If the last one refers to #children (not value), level of first fail
    def equal_to_height(
        self,
        other: MaryTreeNode[T],
        levels_to_check: int,
        sympymode: bool = False,
        permit_child_reorder: bool = True,
        primaryVariable: sympy.Symbol = sympy.Symbol("n"),
        secondaryVariables: list[sympy.Symbol] = [],
    ) -> tuple[bool, bool, bool, int]:
        if levels_to_check < 1:
            raise TypeError("Keep levels_to_check >= 1")

        if (
            levels_to_check > 1
            and len(self.children) != len(other.children)
            and (
                levels_to_check > 2
                or not any(
                    [child.isSubtree for child in other.children]
                )  # If the student used a subtree, they don't need correct number of children.
            )
        ):
            return False, len(other.children) > len(self.children), True, 1
        if not sympymode and self.value != other.value:
            return (
                False,
                False,
                False,
                1,
            )  # Whether one is greater than the other is ill defined for generic objects,
            # default to false since it doesn't matter right now
        if sympymode:
            correctVal, tooBig = MaryTreeNode._sympy_equivalence(
                self.value, other.value, primaryVariable, secondaryVariables
            )
            if not correctVal:
                return False, tooBig, False, 1

        if levels_to_check == 1:
            return True, True, True, 1

        if not permit_child_reorder:
            children_ret = [
                childa.equal_to_height(
                    childb,
                    levels_to_check - 1,
                    sympymode,
                    permit_child_reorder,
                    primaryVariable,
                    secondaryVariables,
                )
                for childa, childb in zip(self.children, other.children)
            ]
            # If any are incorrect, they will be first
            # If multiple are incorrect, the incorrect on upper (lower value) levels are first
            children_ret.sort(key=lambda x: (x[0], x[3]))
            return (
                children_ret[0][0],
                children_ret[0][1],
                children_ret[0][2],
                children_ret[0][3] + 1,
            )
        else:
            children_used = set()  # Make sure we don't let all children equal one correct val (reorder not reuse)
            main_ret = []
            for childa in self.children:
                # Find the most correct of all the other children
                other_ret = [
                    (
                        childa.equal_to_height(
                            childb,
                            levels_to_check - 1,
                            sympymode,
                            permit_child_reorder,
                            primaryVariable,
                            secondaryVariables,
                        ),
                        i,
                        childb.isSubtree,
                    )
                    for i, childb in enumerate(other.children)
                    if i not in children_used
                ]
                other_ret.sort(key=lambda x: (x[0][0], x[0][3]), reverse=True)
                # Add to make sure we don't match to this sub child again, unless it's a subtree
                if not other_ret[0][2]:
                    children_used.add(other_ret[0][1])
                main_ret.append(other_ret[0][0])
            # From main ret, we find the biggest error, and return that one
            # (If no errors returns a correct one)
            main_ret.sort(key=lambda x: (x[0], x[3]))
            return main_ret[0][0], main_ret[0][1], main_ret[0][2], main_ret[0][3] + 1

    # Insert a list of children to the current node.
    def insert_children(self, values: list[T], subtree: bool = False) -> None:
        for v in values:
            self.children.append(MaryTreeNode(v, isSubtree=subtree))

    # Tree.equal_level_fill([a,b,c], 3) yields
    #    a
    # b  b  b
    # ccccccccc
    def equal_level_fill(self, values: list[T], repetititon: int) -> None:
        self.value = values[0]
        if len(values) > 1:
            rest = values[1:]
            for i in range(repetititon):
                newchild = MaryTreeNode(rest[0])
                newchild.equal_level_fill(rest, repetititon)
                self.children.append(newchild)

    # Generate a tree with given levels and children per node, all values are set to None
    @staticmethod
    def gen_none_tree(children_per_node: int, levels: int) -> MaryTreeNode[T]:
        root: MaryTreeNode[T] = MaryTreeNode(None)
        if levels == 1:
            return root
        for _ in range(children_per_node):
            root.children.append(
                MaryTreeNode.gen_none_tree(children_per_node, levels - 1)
            )
        return root

    # Create a tree with the given number of children per node and height. Values are set in a level-order, left-to-right traversal.
    @staticmethod
    def list_tree_gen(
        values: list[T], children_per_node: int, levels: int
    ) -> MaryTreeNode[T]:
        root: MaryTreeNode[T] = MaryTreeNode.gen_none_tree(children_per_node, levels)
        q: Queue = Queue()
        q.put(root)
        i = 0
        while not q.empty():
            node = q.get()
            node.value = values[i]
            for child in node.children:
                q.put(child)
            i += 1
        return root

    @staticmethod
    def _string_to_sympy(
        value: str, legal_vars: list[sympy.Symbol] = [sympy.Symbol("n")]
    ) -> sympy.expr:
        if value == "":
            raise ValueError("Tree Nodes should not be left without a value.")
        if (
            re.search("[l,L][o,O][g,G]", value) is not None
            and re.search("log\(.+,.+\)", value) is None
        ):
            raise ValueError(
                f"The entry ${value}$ does not use the correct format for logarithms. For all logs in the recursion tree, use the format log(a,b) to represent $\\log_b a$. You must explicitly declare a base."
            )
        # Hardcoded because N is a designated sympy function, so the later check won't see it.
        if re.search("N", value) is not None:
            raise ValueError(
                f"Illegal variable N was used in the entry ${value}$. Only include the following variables in your answer: {legal_vars}"
            )
        try:
            val = sympy.parsing.sympy_parser.parse_expr(value, transformations="all")
        except Exception:
            raise ValueError(f"{value} contains invalid expression formatting.")
        for var in val.free_symbols:
            if var not in legal_vars:
                raise ValueError(
                    f"Illegal variable {var} was used in the entry ${value}$. Only include the following variables in your answer: {legal_vars}"
                )
        return val

    @staticmethod
    def from_dict(
        dict_: dict[str, Any],
        cast_func: Callable[[Any], T] = identity,
        grader: bool = False,
    ) -> MaryTreeNode[T]:
        value = dict_["value"]
        valT: T = cast_func(value)
        node: MaryTreeNode[T] = MaryTreeNode(valT)
        node.isSubtree = dict_.get("subtree", False)
        childdata = dict_.get("children", [])

        for child in childdata:
            node.children.append(MaryTreeNode.from_dict(child, cast_func, grader))
        return node

    def to_dict(self) -> dict[str, Any]:
        return {
            "value": self.value,
            "children": [child.to_dict() for child in self.children],
        }

    # returns (isEquivalent, is b>a, asymptotically on primary_var)
    @staticmethod
    def _sympy_equivalence(
        a: Union[sympy.Expr, str],
        b: Union[sympy.Expr, str],
        primary_var: sympy.Symbol = sympy.Symbol("n"),
        secondary_vars: list[sympy.Symbol] = [],
    ) -> tuple[bool, bool]:
        c: sympy.Expr = 0
        d: sympy.Expr = 0
        all_vars = secondary_vars + [primary_var]
        if isinstance(a, str):
            c = MaryTreeNode._string_to_sympy(a, all_vars)
        else:
            c = a
        if isinstance(b, str):
            d = MaryTreeNode._string_to_sympy(b, all_vars)
        else:
            d = b

        limit = sympy.limit(d - c, primary_var, sympy.oo)
        greater = bool(
            limit.subs([(x, 1) for x in limit.free_symbols]) > sympy.sympify(0)
        )
        return sympy.simplify((c) - (d)) == 0, greater

    # Get the lowest level on the tree that has a subtree
    def _subtree_at_max_level(self, level: int = 1) -> tuple[int, Optional[T]]:
        if self.isSubtree:
            return level, self.value

        maxlevel = -1
        maxval = None
        for child in self.children:
            childsub, csubval = child._subtree_at_max_level(level + 1)
            if childsub > maxlevel:
                maxlevel = childsub
                maxval = csubval
        return maxlevel, maxval

    @staticmethod
    def RecurrenceTreeGrader(
        data: su.QuestionData,
        reftree: MaryTreeNode,
        refPerLevel: list[sympy.expr],
        refLeafCount: Optional[sympy.expr] = None,
        refLeafLevelWork: Optional[sympy.expr] = None,
        refHeight: Optional[sympy.expr] = None,
        primaryVariable: sympy.Symbol = sympy.Symbol("n"),  # Matters for feedback
        secondaryVariables: list[
            sympy.Symbol
        ] = [],  # Throws an error if they use illegal symbol
        workPerCallWeight: int = 2,  # How much each of the question elements should be weighted relative to each other
        workPerLevelWeight: int = 2,
        heightWeight: int = 1,
        leafCountWeight: int = 1,
        allOrNothing: bool = False,  # If true, no partial credit
        extraHints: bool = True,  # Tells the student the first incorrect level for WPL and WPC
    ) -> Callable[[Any], tuple[float, str]]:
        def inner_grader(raw_sub: dict[str, Any]) -> tuple[float, str]:
            sub_tree = MaryTreeNode.from_dict(
                raw_sub["WorkPerCall"],
                cast_func=lambda x: MaryTreeNode._string_to_sympy(
                    x, secondaryVariables + [primaryVariable]
                ),
                grader=True,
            )

            levels_to_grade = data["params"]["levels_graded"]
            final_level = data["params"].get("enable-final-level", False)
            enable_height = data["params"].get("enable_height", False)
            grade_wpl = refPerLevel
            wpl_levels_to_grade = levels_to_grade

            # The front-end element treats the total work for the leaves as the first element of the work per level array
            if final_level:
                grade_wpl = [refLeafLevelWork] + refPerLevel
                wpl_levels_to_grade += 1

            feedbackarr = []
            points_possible = (
                workPerCallWeight
                + workPerLevelWeight
                + (leafCountWeight if final_level else 0)
                + (heightWeight if enable_height else 0)
            )
            points_earned = 0

            treeCorrect, nodeTooBig, childCount, wrongLevel = reftree.equal_to_height(
                sub_tree,
                levels_to_grade,
                True,
                primaryVariable=primaryVariable,
                secondaryVariables=secondaryVariables,
            )
            if treeCorrect:
                points_earned += workPerCallWeight
                feedbackarr.append("The work per call recurrence tree is correct")
            else:
                fbstring = "The work per call recurrence tree is not correct."
                if extraHints:
                    if childCount:
                        fbstring += f" At least one node on level {wrongLevel} {'has too many' if nodeTooBig else 'does not have enough'} children."
                    else:
                        fbstring += f" The first incorrect level is {wrongLevel}. "
                        fbstring += f"At least one node's value is {'greater' if nodeTooBig else 'less'} than the correct value."
                feedbackarr.append(fbstring)

            wpl = True
            # The element depends on the work per level array always having one too many elements (the extra is blank), we handle it
            wpl_sub = raw_sub["WorkPerLevel"][:-1]
            if len(wpl_sub) < wpl_levels_to_grade:
                feedbackarr.append(
                    f"Not enough 'work per level' nodes were completed, please complete {levels_to_grade}"
                )
                wpl = False
            else:
                first_wrong = -1
                first_wrong_str = ""
                first_wrong_too_big = False
                for i, (ref, rsub) in enumerate(
                    zip(grade_wpl, wpl_sub[:wpl_levels_to_grade])
                ):
                    correct, tooBig = MaryTreeNode._sympy_equivalence(
                        ref, rsub, primaryVariable, secondaryVariables
                    )
                    wpl = wpl and correct
                    # -1 -> it hasn't been set 0 -> the Final level is wrong
                    if not correct and first_wrong <= 0:
                        first_wrong = i
                        first_wrong_str = rsub
                        first_wrong_too_big = tooBig
                if wpl:
                    feedbackarr.append("The work per level column is correct")
                    points_earned += workPerLevelWeight
                else:
                    extra_wpl_hint = f"{f' The final level input is incorrect: ${first_wrong_str}$' if first_wrong == 0 else f' Level {first_wrong} is the first incorrect entry: ${first_wrong_str}$'} is {'greater' if first_wrong_too_big else 'less'} than the correct answer"
                    feedbackarr.append(
                        f"The work per level column is not correct.{f'{extra_wpl_hint}' if extraHints else ''}"
                    )

            if enable_height:
                heightCorrect, heightTooBig = MaryTreeNode._sympy_equivalence(
                    refHeight, raw_sub["Height"], primaryVariable, secondaryVariables
                )
                if heightCorrect:
                    feedbackarr.append("The tree height is correct")
                    points_earned += heightWeight
                else:
                    heightfb = f"The tree height is not correct: ${raw_sub['Height']}$ "
                    if extraHints:
                        heightfb += f'is {"greater" if heightTooBig else "less"} than the correct answer'
                    feedbackarr.append(heightfb)

            if final_level:
                leafCorrect, leafTooBig = MaryTreeNode._sympy_equivalence(
                    refLeafCount,
                    raw_sub["LeafCount"],
                    primaryVariable,
                    secondaryVariables,
                )
                if leafCorrect:
                    feedbackarr.append("The total number of leaves is correct")
                    points_earned += leafCountWeight
                else:
                    leaffb = f"The total number of leaves is not correct: ${raw_sub['LeafCount']}$ "
                    if extraHints:
                        leaffb += f'is {"greater" if leafTooBig else "less"} than the correct answer'
                    feedbackarr.append(leaffb)

            feedback = "\n".join(feedbackarr)

            if allOrNothing:
                if points_earned == points_possible:
                    return 1, feedback
                else:
                    return 0, feedback

            return (points_earned / points_possible), feedback

        return inner_grader
