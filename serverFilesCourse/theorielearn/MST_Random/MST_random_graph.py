import itertools

import chevron
import networkx as nx
import numpy as np
import prairielearn as pl
from theorielearn.shared_utils import QuestionData, iter_all_strings


def generate_graph(
    data: QuestionData,
    *,
    num_nodes: int = 7,  # The number of nodes in the graph
    min_num_edges: int = 10,  # The number of edges in the graph. Will create more to force full connectivity
    max_edge_weight: int = 20,
):  # All edge weights will be 1-max_edge_weight inclusive
    # set up labels
    labels = list(itertools.islice(iter_all_strings(), num_nodes))
    G = nx.Graph()
    G.add_nodes_from(labels)

    # Set up Graph
    # MST Guarantees a unique solution if edge weights are unique so we use random choice
    # To ensure no replacement on range [1, max_edge_weight]
    # It is also made too long to ensure it remains unique if extra edges are added to make it fully connected
    max_edge_weight = max(max_edge_weight, min_num_edges + num_nodes)
    edgeweights = np.random.choice(
        np.arange(1, max_edge_weight + 1),
        size=(min_num_edges + num_nodes),
        replace=False,
    )
    indexoptions = list(itertools.combinations(labels, 2))
    randgenerator = np.random.default_rng()
    edgelocs = randgenerator.choice(indexoptions, size=min_num_edges, replace=False)
    edgetuples = [
        (source, dest, weight.item())
        for (source, dest), weight in zip(edgelocs, edgeweights)
    ]
    # .item() calls convert np.int64 to int
    G.add_weighted_edges_from(edgetuples)

    # Add edges to ensure we're fully connected
    # uses the same edgeweights as before to insure uniqueness
    toadd = nx.k_edge_augmentation(G, 1)
    weightedtoadd = [
        (From, to, weight.item())
        for (From, to), weight in zip(
            toadd, itertools.islice(edgeweights, min_num_edges, None)
        )
    ]

    edgetuples.extend(weightedtoadd)
    G.add_weighted_edges_from(weightedtoadd)

    for in_node, out_node, edge_data in G.edges(data=True):
        edge_data["label"] = edge_data["weight"]

    # Makes table more visually appealing, on the outside since it will be used multiple times
    sortededgetuples = sorted(edgetuples)
    # Set up table of edge weights
    tabledatalist = [
        {"from": From, "to": to, "weight": weight}
        for From, to, weight in sortededgetuples
    ]

    # Calculate the MST. We keep using sortededgetuples so the answer and the table are in the same order
    MST = nx.minimum_spanning_tree(G)
    checkboxes = [
        {"from": From, "to": to, "weight": weight, "correct": MST.has_edge(From, to)}
        for From, to, weight in sortededgetuples
    ]

    renderdict = {"checkboxes": checkboxes, "tabledatalist": tabledatalist}

    with open(
        data["options"]["server_files_course_path"]
        + "/theorielearn/MST_Random/MST_random_template.html"
    ) as f:
        data["params"]["html"] = chevron.render(f, renderdict).strip()

    data["params"]["netgraph"] = pl.to_json(G)
    data["params"]["labels"] = pl.to_json(labels)
