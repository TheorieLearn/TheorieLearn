import networkx as nx
from theorielearn.graph_construction import server_base
from theorielearn.graph_construction.server_base import GraphConstructionRow, StrEdge
from theorielearn.graphs.graph_utils import generate_pl_graph
from theorielearn.shared_utils import QuestionData


def get_rows_info() -> list[GraphConstructionRow]:
    return [
        GraphConstructionRow(
            "(s, 0, 0)",
            "(v, 1, 0)",
            spec_out_vertex_types=["the starting vertex of a path in G"],
            spec_in_vertex_types=["red"],
        ),
        GraphConstructionRow(
            "(s, 0, 0)",
            "(v, 0, 1)",
            spec_out_vertex_types=["the starting vertex of a path in G"],
            spec_in_vertex_types=["blue"],
        ),
        GraphConstructionRow(
            "(u, r, b)",
            "(v, 1, b)",
            spec_edge_types=[r"edges $u \rightarrow v$ such that $v$ is red"],
        ),
        GraphConstructionRow(
            "(u, r, b)",
            "(v, r, 1)",
            spec_edge_types=[r"edges $u \rightarrow v$ such that $v$ is blue"],
        ),
    ]


def generate(data: QuestionData) -> None:
    part_symbols = ["u", "r", "b"]
    alt_orig_vertex_symbol = "v"
    original_graph = server_base.build_nxdigraph(
        {
            StrEdge("s", "R1"): None,
            StrEdge("s", "R2"): None,
            StrEdge("R1", "R2"): None,
            StrEdge("R2", "B"): None,
            StrEdge("s", "B"): None,
            StrEdge("R2", "B"): None,
        }
    )
    data["params"]["original_graph_json"] = nx.node_link_data(
        original_graph, edges="links"
    )
    data["params"]["original_graph"] = generate_pl_graph(original_graph, rankdir="TB")

    server_base.generate(data, get_rows_info(), part_symbols, alt_orig_vertex_symbol)


def grade(data: QuestionData) -> None:
    part_values = [{"s", "R1", "R2", "B"}, {"0", "1"}, {"0", "1"}]
    part_symbols = ["u", "r", "b"]
    alt_orig_vertex_symbol = "v"
    special_vertices = {
        "red": {"R1", "R2"},
        "blue": {"B"},
        "the starting vertex of a path in G": {"s"},
    }
    special_edges = {
        r"edges $u \rightarrow v$ such that $v$ is red": {
            StrEdge("s", "R1"),
            StrEdge("R1", "R2"),
        },
        r"edges $u \rightarrow v$ such that $v$ is blue": {
            StrEdge("s", "B"),
            StrEdge("R2", "B"),
        },
    }

    server_base.grade(
        data=data,
        original_graph=nx.node_link_graph(
            data["params"]["original_graph_json"], edges="links"
        ),
        part_values=part_values,
        part_symbols=part_symbols,
        alt_orig_vertex_symbol=alt_orig_vertex_symbol,
        special_vertices=special_vertices,
        special_edges=special_edges,
        rows_info=get_rows_info(),
    )
