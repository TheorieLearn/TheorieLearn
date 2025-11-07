import json
import networkx as nx
from theorielearn.graph_construction import server_base
from theorielearn.graph_construction.server_base import GraphConstructionRow, StrEdge
from theorielearn.graphs.graph_utils import generate_pl_graph
from theorielearn.shared_utils import QuestionData


def get_rows_info() -> list[GraphConstructionRow]:
    return [
        GraphConstructionRow(
            "(u, -)",
            "(v, +)",
            alternate_sentence="For each $u \\to v$ edge in $G$, to account for the case that $u = v_i$\
                                    for some odd $i$ in a path, $G'$ should contain the edge",
            special_row_id="-",
        ),
        GraphConstructionRow(
            "(u, +)",
            "(v, -)",
            alternate_sentence="For each $u \\to v$ edge in $G$, to account for the case that $u = v_i$\
                                    for some even $i$ in a path, $G'$ should contain the edge",
            special_row_id="",
        ),
    ]


def generate(data: QuestionData) -> None:
    part_symbols = ["u", "±"]
    alt_orig_vertex_symbol = "v"
    original_graph = server_base.build_nxdigraph(
        {
            StrEdge("s", "a"): "1",
            StrEdge("s", "b"): "2",
            StrEdge("a", "b"): "3",
            StrEdge("a", "t"): "4",
            StrEdge("b", "t"): "5",
        }
    )
    data["params"]["original_graph_json"] = nx.readwrite.node_link_data(
        original_graph, edges="links"
    )

    data["params"]["original_graph"] = generate_pl_graph(original_graph, rankdir="TB")

    server_base.generate(data, get_rows_info(), part_symbols, alt_orig_vertex_symbol)


def add_edge_with_weight(
    out_vertex: str,
    in_vertex: str,
    out_v_orig: str,
    in_v_orig: str,
    generated_graph: nx.DiGraph,
    original_graph: nx.DiGraph,
    special_row_id: str | None,
) -> None:
    orig_edge = original_graph.get_edge_data(out_v_orig, in_v_orig)
    label = "0"
    if orig_edge:
        label = str(orig_edge["label"])
        if special_row_id:
            label = special_row_id + label
    generated_graph.add_edge(out_vertex, in_vertex, label=label)


server_base.add_edge_to_graph = add_edge_with_weight


def grade(data: QuestionData) -> None:
    part_values = [{"s", "a", "b", "t"}, {"+", "-"}]
    part_symbols = ["u", "±"]
    alt_orig_vertex_symbol = "v"

    flipped_signs = [[], ["u", "+"], ["v", "-"], ["u", "-"], ["v", "+"]]
    if all(
        flipped_signs[i]
        == data["submitted_answers"][f"ans{i}"].strip("()").replace(" ", "").split(",")
        for i in range(1, 4)
    ):
        data["feedback"]["flipped"] = (
            "You generated the correct graph structure, but make sure to check the parity!"
        )

    server_base.grade(
        data=data,
        original_graph=nx.readwrite.node_link_graph(
            data["params"]["original_graph_json"], edges="links"
        ),
        part_values=part_values,
        part_symbols=part_symbols,
        special_vertices={},
        special_edges={},
        alt_orig_vertex_symbol=alt_orig_vertex_symbol,
        rows_info=get_rows_info(),
        has_weights=True,
    )
