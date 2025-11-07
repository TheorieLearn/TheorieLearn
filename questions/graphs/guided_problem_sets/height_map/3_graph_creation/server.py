import networkx as nx
from theorielearn.graph_construction import server_base
from theorielearn.graph_construction.server_base import GraphConstructionRow, StrEdge
from theorielearn.graphs.graph_utils import generate_pl_graph
from theorielearn.shared_utils import QuestionData


def get_rows_info() -> list[GraphConstructionRow]:
    return [
        GraphConstructionRow(
            "([i.j], up)",
            "([i'.j'], up)",
            spec_edge_types=[
                r"$|i - i'| + |j - j'| = 1$",
                r"$Elev[i,j] < Elev[i',j'] \leq Elev[i,j] + \Delta$",
            ],
        ),
        GraphConstructionRow(
            "([i.j], up)",
            "([i.j], down)",
            edge_to_same_vertex_in_G=True,
        ),
        GraphConstructionRow(
            "([i.j], down)",
            "([i'.j'], down)",
            spec_edge_types=[
                r"$|i - i'| + |j - j'| = 1$",
                r"$Elev[i,j] > Elev[i',j'] \geq Elev[i,j] - \Delta$",
            ],
        ),
    ]


def generate(data: QuestionData) -> None:
    part_symbols = ["[i.j]", "d"]
    alt_orig_vertex_symbol = "[i'.j']"
    original_graph = server_base.build_nxdigraph(
        {
            StrEdge("[1.1]", "[1.2]"): "22",
            StrEdge("[1.1]", "[2.1]"): "31",
            StrEdge("[1.2]", "[1.1]"): "-22",
            StrEdge("[2.1]", "[1.1]"): "-31",
        }
    )
    data["params"]["original_graph_json"] = nx.node_link_data(
        original_graph, edges="links"
    )
    data["params"]["original_graph"] = generate_pl_graph(original_graph, rankdir="TB")

    server_base.generate(data, get_rows_info(), part_symbols, alt_orig_vertex_symbol)


def grade(data: QuestionData) -> None:
    part_values = [{"[1.1]", "[1.2]", "[2.1]", "[2.2]"}, {"up", "down"}]
    part_symbols = ["[i.j]", "D"]
    alt_orig_vertex_symbol = "[i'.j']"
    special_edges = {
        r"$|i - i'| + |j - j'| = 1$": {
            StrEdge("[1.1]", "[1.2]"),
            StrEdge("[1.2]", "[1.1]"),
            StrEdge("[2.1]", "[1.1]"),
            StrEdge("[1.1]", "[2.1]"),
        },
        r"$Elev[i,j] < Elev[i',j'] \leq Elev[i,j] + \Delta$": {
            StrEdge("[1.1]", "[1.2]")
        },
        r"$Elev[i,j] > Elev[i',j'] \geq Elev[i,j] - \Delta$": {
            StrEdge("[1.2]", "[1.1]")
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
        special_vertices={},
        special_edges=special_edges,
        rows_info=get_rows_info(),
    )
