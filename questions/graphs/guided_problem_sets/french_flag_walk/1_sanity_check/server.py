import random
from typing import List, Optional, Set, Tuple

import networkx as nx
import prairielearn as pl
import theorielearn.shared_utils as su
from theorielearn.graphs.graph_utils import generate_pl_graph


def generate_random_french_graph(
    num_nodes: int,
    num_edges: int,
) -> Tuple[nx.DiGraph, Set[str], int]:
    G: Optional[nx.DiGraph] = None
    ans: Set[str] = set()
    starting_node: int = 0
    while G is None:
        G = nx.gnm_random_graph(num_nodes, num_edges, directed=True)
        assert G is not None

        rng: List[int] = list(range(num_nodes))
        subset: List[int] = random.sample(rng, k=5)
        starting_node = subset[0]
        G.add_edge(subset[0], subset[1], label="red")
        G.add_edge(subset[1], subset[2], label="white")
        G.add_edge(subset[2], subset[3], label="blue")
        G.add_edge(subset[3], subset[2], label="red")
        G.add_edge(subset[2], subset[4], label="white")
        if not nx.is_weakly_connected(G):
            G = None
    for _, _, edge_data in G.edges.data():
        edge_data.setdefault("label", random.choice(["red", "white", "blue"]))
        color = edge_data["label"]
        if color != "white":
            edge_data["color"] = color

    ans = get_answer(G, starting_node)
    return G, ans, starting_node


def get_answer(G: nx.DiGraph, s: int) -> Set[str]:
    def reach(G, s):
        return set(nx.shortest_path_length(G, source=s))

    G_prime = nx.DiGraph()

    for v in G.nodes:
        for i in range(3):
            G_prime.add_node((v, i))

    for u, v in G.edges:
        if G[u][v]["label"] == "red":
            G_prime.add_edge((u, 0), (v, 1))
        elif G[u][v]["label"] == "white":
            G_prime.add_edge((u, 1), (v, 2))
        elif G[u][v]["label"] == "blue":
            G_prime.add_edge((u, 2), (v, 0))
        else:
            raise Exception("Invalid edge color")

    reach_in_G_prime = reach(G_prime, (s, 0))
    answer = {str(v) for (v, i) in reach_in_G_prime}
    return answer


def generate(data: su.QuestionData) -> None:
    nodes = random.randint(6, 7)
    G, ans, start = generate_random_french_graph(nodes, 8)
    data["params"]["graph"] = generate_pl_graph(G, label="label")
    data["params"]["starting_node"] = start
    data["correct_answers"]["ffw"] = f"{{{','.join(ans)}}}"


def grade(data: su.QuestionData) -> None:
    su.grade_question_tokenized(data, "ffw")
    pl.set_weighted_score_data(data)
