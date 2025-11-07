from typing import Dict, FrozenSet, Set

import networkx as nx
from theorielearn.graphs.graph_utils import (
    TSPSolutionsDictT,
    generate_pl_graph,
    generate_tsp_test_case,
    traveling_salesman_dp_optimized_helper,
)
from theorielearn.shared_utils import QuestionData, sized_powerset


def get_set_MST(S: Set[int], G: nx.Graph, start_node: int) -> Dict[FrozenSet[int], int]:
    "Compute the result of the minimum spanning tree, which is the incorrect recurrence"

    memdict: Dict[FrozenSet[int], int] = dict()
    memdict[frozenset()] = 0

    for subset in sized_powerset(S, 1):
        subG = G.subgraph(set(subset))
        mst = nx.minimum_spanning_tree(subG)
        min_dist = mst.size(weight="weight") + min(
            G.edges[(start_node, node)]["weight"] for node in subset
        )

        memdict[frozenset(subset)] = min_dist

    return memdict


def get_memdict_from_tsp_solutions(
    solutions: TSPSolutionsDictT,
) -> Dict[FrozenSet[int], int]:
    memdict: Dict[FrozenSet[int], int] = {
        frozenset(solution_dists.keys()): min(solution_dists.values())
        for solution_dists in solutions.values()
    }
    memdict[frozenset()] = 0

    return memdict


def generate(data: QuestionData) -> None:
    start_node = 0
    num_nodes = 4
    weight_limit = 700

    G = generate_tsp_test_case(num_nodes, weight_limit)
    nodes_list = list(int(node) for node in G.nodes)

    # Get number to city name dictionary
    num_to_cities = {
        nodes_list[0]: "Stontrois",
        nodes_list[1]: "Blacksburg",
        nodes_list[2]: "Westminster",
        nodes_list[3]: "Redding",
    }

    S = set(int(node) for node in G.nodes)
    S.remove(start_node)

    memdict = None
    min_dist_memdict = None
    while memdict is None or min_dist_memdict is None:
        G = generate_tsp_test_case(num_nodes, weight_limit)

        _, solutions = traveling_salesman_dp_optimized_helper(G)
        min_dist_memdict = get_set_MST(S, G, start_node=start_node)

        memdict = get_memdict_from_tsp_solutions(solutions)

        if memdict == min_dist_memdict:
            memdict = None
            min_dist_memdict = None

    # Fill row data
    row_data = []
    for subset in sized_powerset(S, 1):
        # Subset with names
        subset_string = ", ".join(rf"\text{{{num_to_cities[num]}}}" for num in subset)
        subdef_answers_name = f"mindist_{subset}_subdef"
        formula_answers_name = f"mindist_{subset}_formula"

        row_data.append(
            {
                "S": subset_string,
                "subdef_answers_name": subdef_answers_name,
                "formula_answers_name": formula_answers_name,
            }
        )

        data["correct_answers"][subdef_answers_name] = memdict[frozenset(subset)]
        data["correct_answers"][formula_answers_name] = min_dist_memdict[
            frozenset(subset)
        ]

    nx.relabel_nodes(G, num_to_cities, copy=False)
    data["params"]["img"] = generate_pl_graph(G, label="weight")
    data["params"]["row_data"] = row_data
