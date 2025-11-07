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

        (when_node,) = parse_tree.subtrees(lambda x: x.label() == "WHEN")

        if when_node[0] == "always":
            return (
                0,
                "Look at the example above--would DAG-longest-path succeed on that graph?",
            )
        elif when_node[0] == "never":
            return (0, "What about a graph with 1 node? A simple chain?")

        (when2_node,) = parse_tree.subtrees(lambda x: x.label() == "WHEN2")
        (bool_node,) = parse_tree.subtrees(lambda x: x.label() == "BOOL")
        (howmany_node,) = parse_tree.subtrees(lambda x: x.label() == "HOWMANY")

        if (
            when2_node[0] == "can"
            and bool_node[0] == "without"
            and howmany_node[0] == "all"
        ):
            return (1, "Good Job! :)")
        elif when2_node[0] == "can":
            if bool_node[0] == "without":
                if howmany_node[0] == "any":
                    return (
                        0.6,
                        "How would we get to a node if none of its prerequisites were satisfied?",
                    )
                elif howmany_node[0] == "exactly one":
                    return (0.6, "Why exactly one?")
                else:
                    return (0, "")
            elif howmany_node[0] == "exactly one" or howmany_node == "any":
                return (
                    0.8,
                    "Your statement is correct, but why does that imply that DAG-shortest-path won't work?",
                )
            elif bool_node[0] == "only after":
                return (0.4, "What part of DAG-shortest-path imposes this condition?")

        elif when2_node[0] == "will always":
            return (0.3, "Why always? What about the graph above?")
        elif when2_node[0] == "will never":
            return (0.3, "Why never?")
        return (0.0, "")

    grade_question_parameterized(data, "cs374", grade_function)
    pl.set_weighted_score_data(data)
