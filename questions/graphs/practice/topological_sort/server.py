import random
from collections.abc import Callable, Iterable
from itertools import combinations
from typing import TypeVar

import networkx as nx
import prairielearn as pl
import theorielearn.shared_utils as su

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
    num_vertices = 9
    num_edges = 12

    vertices = list(range(num_vertices))
    random.shuffle(vertices)

    possible_edges = [
        (vertices[i], vertices[j]) for (i, j) in combinations(range(num_vertices), 2)
    ]
    edges = random.sample(possible_edges, num_edges)

    graph: nx.DiGraph = nx.DiGraph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(edges)

    data["params"]["graph"] = nx.readwrite.json_graph.node_link_data(
        graph, edges="links"
    )
    data["params"]["img"] = generate_pl_graph(graph)
    data["params"]["possible_answer"] = "".join(map(str, nx.topological_sort(graph)))


def grade(data: pl.QuestionData) -> None:
    graph: nx.DiGraph = nx.readwrite.json_graph.node_link_graph(
        data["params"]["graph"], edges="links"
    )
    grade_toposort(
        data,
        "r",
        graph.nodes,
        graph.edges(),
        lambda x: list(map(int, x.replace(" ", ""))),
    )
    pl.set_weighted_score_data(data)
