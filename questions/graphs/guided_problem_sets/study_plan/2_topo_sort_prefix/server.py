import random

import networkx as nx
import prairielearn as pl
from theorielearn.graphs.graph_utils import grade_toposort
from theorielearn.shared_utils import QuestionData, grade_question_parameterized

random.seed(3)


def generate(data: QuestionData) -> None:
    G = nx.gnp_random_graph(10, 0.5, directed=True)
    DAG = nx.DiGraph(
        [
            (u, v, {"weight": random.randint(-10, 10)})
            for (u, v) in G.edges()
            if u < v and (abs(u - v) < 5)
        ]
    )
    assert nx.is_directed_acyclic_graph(DAG)
    data["params"]["graph"] = nx.node_link_data(DAG, edges="links")
    data["params"]["img"] = pl.to_json(DAG)


def grade(data: QuestionData) -> None:
    DAG = nx.node_link_graph(
        data["params"]["graph"], edges="links"
    )

    if (
        data["submitted_answers"]["ex_topo_sort"] == "2740153968"
        or data["submitted_answers"]["ex_topo_sort"] == "0136247895"
    ):
        data["partial_scores"]["ex_topo_sort"] = {
            "score": 0.0,
            "feedback": "Your response must be different from the examples.",
        }
    else:
        grade_toposort(
            data,
            "ex_topo_sort",
            DAG.nodes,
            DAG.edges,
            lambda x: list(map(int, x.replace(" ", ""))),
        )

    def grade_study_plan_short(submitted_answer) -> tuple[float, str | None]:
        lst = list(submitted_answer)
        if len(lst) != 6:
            return (0, "Wrong number of nodes!")
        elif lst[5] != "6":
            return (0, "Your study plan should end at the target node.")
        for i in range(0, 5):
            if f"{i}" not in lst:
                return (0.3, "Missing one of the required prerequisites!")
        if (
            lst.index("0") > lst.index("1")
            or lst.index("1") > lst.index("3")
            or lst.index("2") > lst.index("4")
        ):
            return (0.6, "You have the correct nodes, but the order is not valid!")
        return (1, "Correct!")

    def grade_study_plan_long(submitted_answer) -> tuple[float, str | None]:
        lst = list(submitted_answer)
        if len(set(lst)) != 9:
            return (
                0,
                "Your study plan is the wrong length or contains duplicate nodes.",
            )
        if lst[-1] != "6":
            return (0, "Your study plan should end at the target node.")
        if "8" in lst:
            return (0, "Your study plan contains a node that depends on the target.")
        if (
            lst.index("0") > lst.index("1")
            or lst.index("1") > lst.index("3")
            or lst.index("1") > lst.index("5")
            or lst.index("3") > lst.index("6")
            or lst.index("2") > lst.index("4")
            or lst.index("4") > lst.index("6")
            or lst.index("7") > lst.index("9")
        ):
            return (0.5, "You have the right nodes, but their order is not valid.")

        return (1, "Correct!")

    grade_question_parameterized(data, "ex_study_plan_short", grade_study_plan_short)
    grade_question_parameterized(data, "ex_study_plan_long", grade_study_plan_long)
    pl.set_weighted_score_data(data)
