from dataclasses import dataclass, field
from typing import List, Union

from nltk.parse import RecursiveDescentParser
from nltk.tree import Tree

from theorielearn.scaffolded_writing.cfg import ScaffoldedWritingCFG

# Note: the ValueError (PARSE_ERROR) is meant to be feedback for the student
# All other exceptions are intended to prevent developer mistakes during question development
PARSE_ERROR = ValueError(
    "Your submission could not be parsed. This error may have been caused by submitting an incomplete response."
)


class AmbiguousParseException(Exception):
    """
    Raised if the CFG is ambiguous and there are multiple ways to parse the student submission.
    """

    pass


class PathCanNeverExistWarning(Exception):
    """
    To guard against potential mistakes (e.g. typos, updating the CFG without updating the grading code),
    this exception is raised if the path specified by the grading code could not *possibly* exist
    in *any* parse tree produced by the CFG. In other words, if a check would always return False on every
    possible student submission, then the person writing the check probably made a mistake, so we should
    raise an alarm about that.
    """

    pass


@dataclass(frozen=True)
class StudentSubmission:
    token_list: List[str]
    cfg: ScaffoldedWritingCFG

    parse_tree: Tree = field(init=False)

    def __post_init__(self) -> None:
        try:
            possible_parse_trees = RecursiveDescentParser(self.cfg).parse_all(
                self.token_list
            )
        except ValueError:
            raise PARSE_ERROR

        if len(possible_parse_trees) == 0:
            raise PARSE_ERROR
        elif len(possible_parse_trees) > 1:
            raise AmbiguousParseException

        # Set parse tree with this because class is frozen
        object.__setattr__(self, "parse_tree", possible_parse_trees[0])

    def does_path_exist(self, *path: str) -> bool:
        """
        If we treat the parse tree as a directed graph where each node is labeled with the string that
        represents the terminal/nonterminal at that node, then this function returns True iff there
        exists a path in the tree whose labels exactly match the specified labels.
        """
        assert len(path) > 0

        if not self.cfg.can_produce_path(*path):
            raise PathCanNeverExistWarning

        # Handle edge case where path is just a single terminal
        if len(path) == 1 and path[0] in self.token_list:
            return True

        path_list = list(path)

        def does_path_exist_starting_from_node(
            path_index: int, node: Union[Tree, str]
        ) -> bool:
            # If string case, must be at the end of the path
            if isinstance(node, str):
                return (
                    path_index == len(path_list) - 1 and path_list[path_index] == node
                )

            # If we read the whole list, return true
            if path_index == len(path_list) - 1:
                return path_list[path_index] == node.label()

            # Check that the label matches and recurse
            if path_list[path_index] != node.label():
                return False

            return any(
                does_path_exist_starting_from_node(path_index + 1, child)
                for child in node
            )

        return any(
            does_path_exist_starting_from_node(0, node)
            for node in self.parse_tree.subtrees()
        )
