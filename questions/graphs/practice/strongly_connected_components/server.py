from collections.abc import Callable, Iterable
from typing import TypeVar

import networkx as nx
import prairielearn as pl
import theorielearn.shared_utils as su
from networkx import Graph

VertexT = TypeVar("VertexT")


def generate_pl_graph(
    g: nx.DiGraph | nx.Graph, label: str | None = None, rankdir: str = "LR"
) -> str:
    """
    Generates a string usable by a pl-graph element.
    @param graph nx.DiGraph
        graph to construct string representation of
    @return str
        representation of graph usable by a pl-graph element
    """
    visualize_graph = nx.nx_agraph.to_agraph(g)
    visualize_graph.graph_attr["rankdir"] = rankdir

    if label:
        for u, v in visualize_graph.edges():
            edge = visualize_graph.get_edge(u, v)
            edge.attr["label"] = edge.attr[label]

    return visualize_graph.to_string()


def grade_toposort(
    data: pl.QuestionData,
    question_name: str,
    vertices: Iterable[VertexT],
    edges: Iterable[tuple[VertexT, VertexT]],
    transformation_function: Callable[[str], list[VertexT]],
) -> None:
    """
    Takes in data dictionary and checks if submission for topological ordering is correct.
    The submission is checked against the vertices and edges to check if it follows a valid topological ordering.
    transformation_function is used in order to handle multiple submission formats (comma separated list, just integers, etc).
    """

    def grader(submission: str) -> tuple[bool, str]:
        """
        The grader function takes in the submission and sets it as correct/incorrect, with feedback messages.
        """
        transformed_submission = transformation_function(submission)
        if not (
            set(transformed_submission) == set(vertices)
            and len(transformed_submission) == len(list(vertices))
        ):
            return (
                False,
                "Your input does not contain all vertices of the graph exactly once, or it contains vertices which are not in the graph.",
            )
        for i, j in edges:
            if transformed_submission.index(j) < transformed_submission.index(i):
                return False, f"The edge ({i},{j}) is not respected in your ordering."
        return True, "That's correct!"

    su.grade_question_parameterized(data, question_name, grader)


def generate(data: pl.QuestionData) -> None:
    num_sscs = 0
    isolated = 1
    n = 10
    m = 12
    while num_sscs < 4 or num_sscs > 6 or isolated != 0:
        g = nx.gnm_random_graph(n, m, seed=None, directed=True)
        meta_graph = nx.condensation(g)
        isolated = len(list(nx.isolates(g)))
        num_sscs = meta_graph.number_of_nodes()

    # Spread out edges so they're easier to see
    mapping: dict[int, str] = {
        n: "".join(map(str, sorted(meta_graph.nodes[n]["members"]))) for n in meta_graph
    }
    meta_graph_relabeled: Graph = nx.relabel_nodes(meta_graph, mapping, copy=False)

    data["correct_answers"]["meta_v"] = ", ".join(map(str, meta_graph_relabeled.nodes))
    data["correct_answers"]["meta_e"] = ", ".join(
        f"{u}->{v}" for u, v in meta_graph_relabeled.edges
    )
    data["correct_answers"]["meta_topo"] = ", ".join(
        map(str, nx.topological_sort(nx.DiGraph(meta_graph_relabeled)))
    )

    data["params"]["img"] = generate_pl_graph(g)
    data["params"]["meta_v"] = list(meta_graph_relabeled.nodes)
    data["params"]["meta_e"] = list(meta_graph_relabeled.edges)


def parse(data: pl.QuestionData) -> None:
    # First, process the submitted vertices
    meta_v = data["submitted_answers"]["meta_v"]
    if meta_v:
        data["submitted_answers"]["meta_v"] = ", ".join(
            "".join(sorted(i)) for i in (su.tokenize_string(meta_v))
        )

    # Next, process the submitted toposort
    meta_topo = data["submitted_answers"]["meta_topo"]
    if meta_topo:
        data["submitted_answers"]["meta_topo"] = ", ".join(
            "".join(sorted(i)) for i in (su.tokenize_string(meta_topo))
        )

    # Finally, process the submitted edges
    meta_e = data["submitted_answers"]["meta_e"]
    if meta_e:
        edge_list = meta_e.replace(" ", "").split(",")
        new_edge_arr = []
        for edge in edge_list:
            new_edge = ["".join(sorted(v)) for v in edge.split("->")]
            new_edge_arr.append("->".join(new_edge))
        data["submitted_answers"]["meta_e"] = ", ".join(new_edge_arr)


def grade(data: pl.QuestionData) -> None:
    su.grade_question_tokenized(data, "meta_v")
    su.grade_question_tokenized(data, "meta_e")

    vertices = data["params"]["meta_v"]
    edges = data["params"]["meta_e"]

    grade_toposort(data, "meta_topo", vertices, edges, su.tokenize_string)

    pl.set_weighted_score_data(data)
