from typing import Callable, List, Optional, Tuple

import theorielearn.graphs.graph_utils as gu
import networkx as nx
import pytest

# ------------------------ Graph Helper Tests ----------------------------------

EdgeT = Tuple[int, int, Optional[int]]
EdgeListT = List[EdgeT]
WEIGHT_IDX = 2

# Graph edge lists for tests

EDGES_TEST_GRAPH_ONE_UNWEIGHTED: EdgeListT = [
    (0, 1, None),
    (1, 0, None),
    (1, 2, None),
    (2, 3, None),
    (3, 4, None),
    (4, 2, None),
    (5, 0, None),
]

EDGES_TEST_GRAPH_NO_NEGATIVE_CYCLE: EdgeListT = [
    (0, 1, 0),
    (2, 1, 14),
    (1, 0, 0),
    (1, 4, 3),
    (4, 0, 3),
    (2, 3, 1),
]

# 0 -> 1, 1 -> 0 forms the shortest negative cycle.
EDGES_TEST_GRAPH_SHORTEST_NEGATIVE_CYCLE_LENGTH_TWO: EdgeListT = [
    (0, 1, 0),
    (1, 0, -1),
    (1, 2, 2),
    (2, 3, 4),
    (3, 4, 25),
    (4, 2, 3),
    (5, 0, -29),
]

# 1 -> 2, 2 -> 3, 3 -> 4, 4 -> 4 forms the shortest negative cycle.
EDGES_TEST_GRAPH_SHORTEST_NEGATIVE_CYCLE_LENGTH_FOUR: EdgeListT = [
    (0, 1, 2),
    (1, 2, -1),
    (2, 3, -4),
    (3, 4, 1),
    (4, 1, 0),
    (4, 0, -1),
]


def generate_test_graph(edges: EdgeListT) -> nx.DiGraph:
    "Generates test graph from edge list"
    ith_weight_is_none = map(lambda x: x[WEIGHT_IDX] is None, edges)
    all_unweighted = all(ith_weight_is_none)
    if any(ith_weight_is_none) and not all_unweighted:
        raise ValueError(
            "Graph has inconsistent weighting" "(only some edeges have weights)"
        )

    graph = nx.DiGraph()

    if all_unweighted:
        graph.add_edges_from(map(lambda x: x[:WEIGHT_IDX], edges))
    else:
        graph.add_weighted_edges_from(edges)

    return graph


# End Graph edge lists and helper


class VerifyGetWeightOfCycle:
    @pytest.mark.parametrize(
        "cycle", [[0, 1, 0], [], [0], [0, 1, 2, 3, 4, 5], [2, 1, 0]]
    )
    def verify_get_weight_of_cycle_exception(self, cycle: List[int]):
        with pytest.raises(ValueError):
            graph = generate_test_graph(
                EDGES_TEST_GRAPH_SHORTEST_NEGATIVE_CYCLE_LENGTH_TWO
            )
            gu.get_weight_of_cycle(graph, cycle)

    @pytest.mark.parametrize(
        "edges, cycle, expected_weight",
        [
            (EDGES_TEST_GRAPH_SHORTEST_NEGATIVE_CYCLE_LENGTH_TWO, [0, 1], -1),
            (EDGES_TEST_GRAPH_SHORTEST_NEGATIVE_CYCLE_LENGTH_TWO, [3, 4, 2], 32),
            (EDGES_TEST_GRAPH_SHORTEST_NEGATIVE_CYCLE_LENGTH_FOUR, [1, 2, 3, 4], -4),
        ],
    )
    def verify_get_weight_of_cycle(
        self, edges: EdgeListT, cycle: List[int], expected_weight: int
    ) -> None:
        graph = generate_test_graph(edges)
        assert gu.get_weight_of_cycle(graph, cycle) == expected_weight


@pytest.mark.parametrize(
    "edges, shortest_negative_cycle_length",
    [
        ([], None),
        (EDGES_TEST_GRAPH_NO_NEGATIVE_CYCLE, None),
        (EDGES_TEST_GRAPH_SHORTEST_NEGATIVE_CYCLE_LENGTH_TWO, 2),
        (EDGES_TEST_GRAPH_SHORTEST_NEGATIVE_CYCLE_LENGTH_FOUR, 4),
    ],
)
def verify_get_edge_count_of_shortest_negative_cycle(
    edges: EdgeListT, shortest_negative_cycle_length: Optional[int]
) -> None:
    graph = generate_test_graph(edges)
    assert (
        gu.get_edge_count_of_shortest_negative_cycle(graph)
        == shortest_negative_cycle_length
    )


def traveling_salesman_brute_force_testing(G: nx.Graph) -> int:
    return gu.traveling_salesman_brute_force(G)[1]


@pytest.mark.parametrize(
    "tsp_solver",
    [gu.traveling_salesman_dp_optimized],
)
def verify_traveling_salesman(tsp_solver: Callable[[nx.Graph], int]) -> None:
    iterations = 10
    n = 6  # These algorithms are VERY inefficient, keep this number small
    weight_limit = 10000
    for _ in range(iterations):
        G = gu.generate_tsp_test_case(n, weight_limit)
        assert traveling_salesman_brute_force_testing(G) == tsp_solver(G)


@pytest.mark.parametrize(
    "tsp_solver",
    [gu.traveling_salesman_dp_optimized, traveling_salesman_brute_force_testing],
)
def verify_traveling_salesman_static(tsp_solver: Callable[[nx.Graph], int]) -> None:
    G = nx.Graph()
    G.add_edge(0, 1, weight=10)
    G.add_edge(0, 2, weight=15)
    G.add_edge(0, 3, weight=20)

    G.add_edge(1, 2, weight=35)
    G.add_edge(1, 3, weight=25)

    G.add_edge(2, 3, weight=30)

    assert tsp_solver(G) == 80


@pytest.mark.parametrize(
    "V, E",
    [(128, 512), (256, 1024), (512, 2048)],
)
def verify_generate_dag(V: int, E: int) -> None:
    yes = gu.generate_dag_with_hamiltonian_path(V, E)
    no = gu.generate_dag_without_hamiltonian_path(V, E)

    assert nx.is_directed_acyclic_graph(yes)
    assert nx.is_directed_acyclic_graph(no)


@pytest.mark.parametrize(
    "V, E",
    [(128, 512), (256, 1024), (512, 2048)],
)
def verify_generate_dag_node_ct(V: int, E: int) -> None:
    yes = gu.generate_dag_with_hamiltonian_path(V, E)
    no = gu.generate_dag_without_hamiltonian_path(V, E)

    assert len(yes.nodes) == V
    assert len(no.nodes) == V


@pytest.mark.parametrize(
    "V, E",
    [(128, 512), (256, 1024), (512, 2048)],
)
def verify_generate_dag_edge_ct(V: int, E: int) -> None:
    yes = gu.generate_dag_with_hamiltonian_path(V, E)
    no = gu.generate_dag_without_hamiltonian_path(V, E)

    assert len(yes.edges) == E
    assert len(no.edges) == E


@pytest.mark.parametrize(
    "V, E",
    [(128, 512), (256, 1024), (512, 2048)],
)
def verify_generate_dag_source_sink(V: int, E: int) -> None:
    G = gu.generate_dag_without_hamiltonian_path(V, E)
    num_sink_nodes = sum(
        1 for _, outdegree in G.out_degree(G.nodes()) if outdegree == 0
    )
    num_source_nodes = sum(1 for _, indegree in G.in_degree(G.nodes()) if indegree == 0)
    assert num_sink_nodes == 1
    assert num_source_nodes == 1
