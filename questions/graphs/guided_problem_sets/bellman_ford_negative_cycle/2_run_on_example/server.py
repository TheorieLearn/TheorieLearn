import math
import random
from typing import Any, Dict, List, Optional, Set, Tuple

import networkx as nx
import prairielearn as pl
from theorielearn.graphs.graph_utils import (
    generate_pl_graph,
    get_edge_count_of_shortest_negative_cycle,
    get_weight_of_cycle,
)
from theorielearn.shared_utils import get_partial_score, grade_question_parameterized

NUM_NODES = 5
NUM_EDGES = 9


def generate_random_weighted_graph(num_nodes: int, num_edges: int) -> nx.DiGraph:
    """
    Generates a random graph with specified numbers of nodes and edges.
    Each edge has a nonzero integer weight in the range [-10, 10].
    @param num_nodes int
        number of nodes
    @param num_edge
        number of edges
    @return nx.DiGraph
        Graph with num_nodes nodes and num_edges edges
    """
    G = nx.gnm_random_graph(num_nodes, num_edges, directed=True)

    for edge in G.edges():
        edge_weight = random.choice([random.randint(-10, -1), random.randint(1, 10)])
        G[edge[0]][edge[1]]["weight"] = edge_weight

    return G


def get_potential_source_vertices(G: nx.DiGraph) -> Set[int]:
    """
    Find all nodes that are ancestors of nodes in negative cycles and not part of any negative cycle.
    For this question, we treat these as potential source vertices for running Bellman-Ford.
    @param G nx.Digraph
        graph to find source nodes for
    @return Set[int]
        set of integers representing all possible source nodes
    """
    potential_source_vertices = set()

    negative_cycles = [
        cycle
        for cycle in nx.simple_cycles(G)
        if get_weight_of_cycle(G, cycle) < 0
    ]

    # Find nodes that are ancestors of nodes in negative cycles.
    for source in G.nodes():
        for cycle in negative_cycles:
            node_in_cycle = cycle[0]
            if source not in cycle and node_in_cycle in nx.descendants(
                G, source
            ):
                potential_source_vertices.add(source)

    # Remove nodes that are in negative cycles.
    source_nodes_in_negative_cycles = set()
    for source in potential_source_vertices:
        for cycle in negative_cycles:
            if source in cycle:
                source_nodes_in_negative_cycles.add(source)

    return potential_source_vertices.difference(source_nodes_in_negative_cycles)


def generate(data: pl.QuestionData) -> None:
    G = generate_random_weighted_graph(NUM_NODES, NUM_EDGES)
    count = get_edge_count_of_shortest_negative_cycle(G)
    while count is None or count < 3 or len(get_potential_source_vertices(G)) == 0:
        G = generate_random_weighted_graph(NUM_NODES, NUM_EDGES)
        count = get_edge_count_of_shortest_negative_cycle(G)

    data["params"]["graph"] = nx.node_link_data(G, edges="links")
    data["params"]["graph_data"] = generate_pl_graph(G, label="weight")
    data["params"]["source_vertex"] = random.choice(
        list(get_potential_source_vertices(G))
    )


def grade_negative_cycle_detection(data: pl.QuestionData) -> None:
    G = nx.node_link_graph(data["params"]["graph"], edges="links")

    transform_cycle = lambda x: [int(node) for node in x.split(",")]

    def grade_cycle_question(cycle: List[int]) -> Tuple[bool, Optional[str]]:
        try:
            if get_weight_of_cycle(G, transform_cycle(cycle)) < 0:
                return (True, None)
            else:
                return (
                    False,
                    "The cycle you've entered does not have negative weight.",
                )
        except ValueError as e:
            return (False, str(e))

    def grade_cycle_weight_question(cycle_weight: int) -> Tuple[bool, Optional[str]]:
        try:
            cycle = transform_cycle(data["submitted_answers"]["cycle-sequence"])
            correct_cycle_weight = get_weight_of_cycle(G, cycle)

            if cycle_weight < 0 and cycle_weight == correct_cycle_weight:
                return (True, None)
            elif cycle_weight == correct_cycle_weight:
                return (
                    False,
                    "Your weight computation was correct, but you didn't identify a negative cycle.",
                )
            else:
                return (False, "Incorrect weight for cycle given.")
        except ValueError as e:
            return (False, str(e))

    grade_question_parameterized(
        data, "cycle-sequence", grade_cycle_question, feedback_field_name="cycle"
    )
    grade_question_parameterized(
        data,
        "negative-cycle-weight",
        grade_cycle_weight_question,
        feedback_field_name="cycle",
    )


def grade_bellman_ford_computation(data: pl.QuestionData) -> bool:
    G = nx.node_link_graph(data["params"]["graph"], edges="links")
    start = data["params"]["source_vertex"]
    end = int(data["submitted_answers"]["node-id-1"])

    # Run Bellman-Ford.
    min_distances = [
        [math.inf for _ in range(len(G.nodes()) + 1)] for _ in range(len(G.nodes))
    ]
    min_distances[start][0] = 0
    edges = []

    for edge in G.edges():
        edges.append((edge[0], edge[1], G[edge[0]][edge[1]]["weight"]))

    for max_edge_count in range(1, len(G.nodes()) + 1):
        for node in range(len(G.nodes())):
            min_distances[node][max_edge_count] = min_distances[node][
                max_edge_count - 1
            ]

        for source, destination, weight in edges:
            if (
                min_distances[source][max_edge_count - 1] + weight
                < min_distances[destination][max_edge_count]
            ):
                min_distances[destination][max_edge_count] = (
                    min_distances[source][max_edge_count - 1] + weight
                )

    # Check if inequality stated in problem holds.
    if min_distances[end][len(G.nodes())] < min_distances[end][len(G.nodes()) - 1]:
        lesser_weight = min_distances[end][len(G.nodes())]
        grade_question_parameterized(
            data, "lesser-weight", lambda x: (x == lesser_weight, None)
        )

        greater_weight = min_distances[end][len(G.nodes()) - 1]
        grade_question_parameterized(
            data, "greater-weight", lambda x: (x == greater_weight, None)
        )
        return True
    return False


def zero_out_dist_scores(data: pl.QuestionData) -> None:
    fields = [
        "lesser-weight",
        "node-id-1",
        "edge-count-1",
        "node-id-2",
        "edge-count-2",
        "greater-weight",
    ]
    for field in fields:
        grade_question_parameterized(data, field, lambda _: (False, None))


def grade_dist_equation(data: pl.QuestionData) -> None:
    destination_node = int(data["submitted_answers"]["node-id-1"])
    G = nx.node_link_graph(data["params"]["graph"], edges="links")

    grade_question_parameterized(data, "edge-count-1", lambda x: (x == NUM_NODES, None))
    grade_question_parameterized(
        data, "edge-count-2", lambda x: (x == NUM_NODES - 1, None)
    )

    if (
        get_partial_score(data, "edge-count-1") == 1
        and get_partial_score(data, "edge-count-2") == 1
        and data["submitted_answers"]["node-id-1"]
        == data["submitted_answers"]["node-id-2"]
        and destination_node in G.nodes()
    ):
        for field in ["node-id-1", "node-id-2"]:
            grade_question_parameterized(data, field, lambda _: (True, None))

        does_satisfy_inequality = grade_bellman_ford_computation(data)
        if not does_satisfy_inequality:
            data["feedback"]["dist"] = (
                "The true values of the subproblems you've selected do not satisfy the inequality."
            )
            zero_out_dist_scores(data)
    else:
        data["feedback"]["dist"] = (
            "Recall from the previous page that, to detect a negative cycle, \nthe Bellman-Ford algorithm needs to find a vertex $v$ such that \n$dist(v, n) < dist(v, n - 1)$. \nWhat is the value of $n$ for the example graph in this problem?"
        )
        zero_out_dist_scores(data)


def grade(data: pl.QuestionData) -> None:
    grade_negative_cycle_detection(data)
    grade_dist_equation(data)
    pl.set_weighted_score_data(data)
