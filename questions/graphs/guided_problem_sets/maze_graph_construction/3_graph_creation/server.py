import networkx as nx
from theorielearn.graph_construction import server_base
from theorielearn.graph_construction.server_base import GraphConstructionRow, StrEdge
from theorielearn.graphs.graph_utils import generate_pl_graph
from theorielearn.shared_utils import QuestionData


def get_rows_info() -> list[GraphConstructionRow]:
    return [
        GraphConstructionRow(
            "(u, h, F)",
            "(v, h, E)",
            spec_edge_types=["high-risk"],
            avoid_spec_edge_types=["hieroglyphics"],
        ),
        GraphConstructionRow(
            "(u, h, c)",
            "(v, S, c)",
            spec_edge_types=["hieroglyphics"],
            avoid_spec_edge_types=["high-risk"],
        ),
        GraphConstructionRow(
            "(u, h, F)", "(v, S, E)", spec_edge_types=["high-risk", "hieroglyphics"]
        ),
        GraphConstructionRow(
            "(u, h, c)",
            "(v, h, c)",
            avoid_spec_edge_types=["high-risk", "hieroglyphics"],
        ),
        GraphConstructionRow(
            "(u, h, E)",
            "(u, h, F)",
            spec_out_vertex_types=["a charging station"],
            spec_in_vertex_types=["a charging station"],
            edge_to_same_vertex_in_G=True,
        ),
    ]


def generate(data: QuestionData) -> None:
    part_symbols = ["u", "h", "c"]
    alt_orig_vertex_symbol = "v"
    original_graph = server_base.build_nxdigraph(
        {
            StrEdge("s", "t"): "R",
            StrEdge("t", "s"): "H",
            StrEdge("s", "a"): None,
            StrEdge("a", "s"): None,
        }
    )
    data["params"]["original_graph_json"] = nx.node_link_data(
        original_graph, edges="links"
    )
    data["params"]["original_graph"] = generate_pl_graph(original_graph, rankdir="TB")

    server_base.generate(data, get_rows_info(), part_symbols, alt_orig_vertex_symbol)


def grade(data: QuestionData) -> None:
    part_values = [{"s", "a", "t"}, {"NS", "S"}, {"F", "E"}]
    part_symbols = ["u", "h", "c"]
    alt_orig_vertex_symbol = "v"
    special_vertices = {"a charging station": {"a"}}
    special_edges = {
        "hieroglyphics": {StrEdge("t", "s")},
        "high-risk": {StrEdge("s", "t")},
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
