from typing import Any

import prairielearn as pl
from nltk.parse import RecursiveDescentParser
from theorielearn.scaffolded_writing.cfg import ScaffoldedWritingCFG
from theorielearn.shared_utils import QuestionData, grade_question_parameterized


def grade(data: QuestionData) -> None:
    def grade_function(tokens: Any) -> tuple[float, str | None]:
        cfg = ScaffoldedWritingCFG.fromstring(
            data["params"]["scaffolded_writing"]["cs374"]["cfg_transition_string"]
        )

        parsed_tree_list = RecursiveDescentParser(cfg).parse_all(tokens)

        if parsed_tree_list is None or len(parsed_tree_list) == 0:
            raise ValueError("Invalid CFG")

        # pick the first parse tree
        parse_tree = parsed_tree_list[0]

        (when_node,) = parse_tree.subtrees(lambda x: x.label() == "WHEN_RELATIVE_TO")

        if when_node[0] == "after":
            return (
                0,
                "Remember $t$ is our target--we don't need to study anything after it!",
            )

        (property_node,) = parse_tree.subtrees(lambda x: x.label() == "PROPERTY")
        (place_node,) = parse_tree.subtrees(lambda x: x.label() == "PLACE")
        (struct_node,) = parse_tree.subtrees(lambda x: x.label() == "STRUCTURE")
        (struct2_node,) = parse_tree.subtrees(lambda x: x.label() == "STRUCTURE2")

        if property_node[0] == "in the same strong component as":
            return (
                0.1,
                "Remember G is already a DAG, so each strong component is exactly one node.",
            )
        elif property_node[0] == "in a cycle with":
            return (0.1, 'G is a DAG! Remember the "A" in "DAG" stands for acyclic...')
        elif property_node[0] == "listed before" or property_node[0] == "listed after":
            if struct_node[0] == "G" or (
                struct_node[0] == "the reversal of"
                and (struct2_node[0] == "G" or struct2_node[0] == "the reversal of G")
            ):
                return (0, 'How can one node be listed "before" another in a graph?')
            return (
                0.6,
                "You're on the right track, but remember this is an if and only if statement--we don't want to study any unnecessary topics.",
            )

        elif property_node[0] == "reachable from":
            if place_node[0] == "t":
                if struct_node[0] == "the reversal of":
                    if struct2_node[0] == "G":
                        return (1, "Good job! :)")
                    elif struct2_node[0] == "A topological sort of G":
                        return (
                            0.6,
                            'How is a node "reachable" from another in a topological sort?',
                        )
                    else:
                        return (0.5, "What's the point of reversing G twice?")

                elif struct_node[0] == "G":
                    return (
                        0.6,
                        "Remember, children of a node are reachable from that node, but ancestors are not.",
                    )
            elif place_node[0] == "a source vertex" or place_node[0] == "a sink vertex":
                return (0, "")
            elif (
                struct_node[0] == "a topological sort of G"
                or struct_node[0] == "a topological sort of a topological sort of G"
                or struct_node[0] == "a topological sort of the reversal of G"
            ):
                return (
                    0,
                    'How is a node "reachable" from another in a topological sort?',
                )
        return (0, "")

    grade_question_parameterized(data, "cs374", grade_function)
    pl.set_weighted_score_data(data)
