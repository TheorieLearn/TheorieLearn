import itertools
from itertools import chain

import chevron
import networkx as nx
import numpy as np
import prairielearn as pl
from theorielearn.shared_utils import QuestionData, iter_all_strings


def generate_graph(
    data: QuestionData,
    *,
    num_nodes: int = 7,  # The number of nodes in the graph
    min_num_edges: int = 10,  # The number of edges in the graph. May create more if force_reachable is True
    max_edge_weight: int = 20,  # All edge weights will be 1-max_edge_weight inclusive
    allow_self_loops: bool = True,  # If False, no nodes will have edges to themselves
    force_reachable: bool = True,
):  # If True, will determine if graph has any unreachable nodes and will create edges
    #  To compensate. A minimal graph will be created if nodes=0 force_reachable=True
    #  If False, some states may remain unreachable and will not part of the answer

    # Set up Graph
    # The leading space ensures Start is sorted first in the table.
    labels = [" Start"] + list(itertools.islice(iter_all_strings(), num_nodes - 1))
    DG = nx.DiGraph()
    DG.add_nodes_from(labels)

    indexoptions = [
        (i, j) for i in labels for j in labels if allow_self_loops or i != j
    ]
    randgenerator = np.random.default_rng()
    edgelocs = randgenerator.choice(indexoptions, size=min_num_edges, replace=False)
    edgetuples = [
        (source, dest, np.random.randint(1, max_edge_weight + 1))
        for source, dest in edgelocs
    ]

    DG.add_weighted_edges_from(edgetuples)

    if force_reachable:
        # Do BFS do determine how many connected reachable components we have
        # And add edges until every node is reachable
        toadd = []
        visited = {label: False for label in labels}

        def BFS(startnode):
            nodelist = nx.bfs_layers(DG, startnode)
            for node in chain.from_iterable(nodelist):
                visited[node] = True

        for label in labels:
            if not visited[label]:
                if label != labels[0]:  # this is fine if its the start node
                    # add an edge from a random node that has already been visited to this one
                    toadd.append(
                        (
                            np.random.choice(
                                [node for node, value in visited.items() if value]
                            ),
                            label,
                            np.random.randint(1, max_edge_weight + 1),
                        )
                    )
                BFS(label)

        DG.add_weighted_edges_from(toadd)
        edgetuples.extend(toadd)

    for in_node, out_node, edge_data in DG.edges(data=True):
        edge_data["label"] = edge_data["weight"]

    # Set up table of edge weights

    tabledatalist = [
        {"from": From, "to": to, "weight": weight}
        for From, to, weight in sorted(edgetuples)
    ]

    # Run Dijkstras to determine correct answers
    totallen = nx.single_source_dijkstra_path_length(DG, labels[0])
    answers = []
    # The order blocks requires a non-strictly increasing ranking for every
    # correct answer. The distance fulfills this trait
    for label in labels:
        if label in totallen:
            # Plus one because the actual length is unimportant and a 0
            # For start registers as false in the mustache conditional
            answers.append({"label": label, "ranking": totallen[label] + 1})
        else:
            answers.append({"label": label})

    renderdict = {"answers": answers, "tabledatalist": tabledatalist}

    with open(
        data["options"]["server_files_course_path"]
        + "/theorielearn/dijkstra_random/dijkstra_random_template.html"
    ) as f:
        data["params"]["html"] = chevron.render(f, renderdict).strip()

    data["params"]["netgraph"] = pl.to_json(DG)
    data["params"]["labels"] = pl.to_json(labels)
