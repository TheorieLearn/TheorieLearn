import html
import os
from copy import deepcopy
from dataclasses import dataclass
from itertools import islice, product
from typing import Any, Optional

import chevron
import networkx as nx
import theorielearn.shared_utils as su
from theorielearn.graphs.graph_utils import generate_pl_graph
from theorielearn.shared_utils import QuestionData


@dataclass(slots=True)
class StrEdge:
    # Retain hashing from parent after __str__ definition.
    __hash__ = object.__hash__

    outgoing: str
    incoming: str

    def __str__(self) -> str:
        return f"(outgoing: {self.outgoing}, incoming: {self.incoming})"


@dataclass(slots=True)
class GraphConstructionRow:
    correct_answer_outgoing: str
    correct_answer_incoming: str
    spec_out_vertex_types: Optional[list[str]] = None
    spec_in_vertex_types: Optional[list[str]] = None
    spec_edge_types: Optional[list[str]] = None
    avoid_spec_out_vertex_types: Optional[list[str]] = None
    avoid_spec_in_vertex_types: Optional[list[str]] = None
    avoid_spec_edge_types: Optional[list[str]] = None
    # used if the default sentence construction is not suitable for the specific question.
    alternate_sentence: Optional[str] = None
    # if True, it means the edge in G' is for every u in G rather than for every u -> v in G.
    edge_to_same_vertex_in_G: bool = False
    special_row_id: Optional[str] = None


def visual_transform_graph(
    G: nx.DiGraph, filled_color: str = "#ADD8E6", shape: str = "box"
) -> nx.DiGraph:
    for _, node_data in G.nodes(data=True):
        node_data["style"] = "filled"
        node_data["color"] = filled_color
        node_data["shape"] = shape
    return G


def build_nxdigraph(
    edges_labels: dict[StrEdge, Optional[str]],
    filled_color: str = "#ADD8E6",
    shape: str = "box",
) -> nx.DiGraph:
    graph = nx.DiGraph()
    for edge, label in edges_labels.items():
        if label:
            graph.add_edge(edge.outgoing, edge.incoming, label=label)
        else:
            graph.add_edge(edge.outgoing, edge.incoming)
    return visual_transform_graph(graph, filled_color, shape)


def get_complete_attributes_sentence(
    out_vertex_attributes: str,
    in_vertex_attributes: str,
    avoid_out_vertex_attributes: str,
    avoid_in_vertex_attributes: str,
    edge_attributes: str,
    avoid_edge_attributes: str,
    orig_vertex_symbol: str,
    alt_orig_vertex_symbol: str,
) -> str:
    """
    Construct the part of the english sentence pertaining to this row of inputs and the attributes of the vertices and edges.
    """
    edge_attributes_str = " that includes " + edge_attributes if edge_attributes else ""
    connection_1 = " and " if edge_attributes and avoid_edge_attributes else ""
    avoid_edge_attributes_str = (
        " that does not include " + avoid_edge_attributes
        if avoid_edge_attributes
        else ""
    )
    edge_attributes_sentence = (
        edge_attributes_str + connection_1 + avoid_edge_attributes_str
    )

    orig_vertex_symbol = (
        f"${orig_vertex_symbol}$"
        if out_vertex_attributes or avoid_out_vertex_attributes
        else ""
    )
    out_vertex_attributes_str = (
        " is " + out_vertex_attributes if out_vertex_attributes else ""
    )
    connection_2 = (
        " and " if out_vertex_attributes and avoid_out_vertex_attributes else ""
    )
    avoid_out_vertex_attributes_str = (
        " is not " + avoid_out_vertex_attributes if avoid_out_vertex_attributes else ""
    )
    out_vertex_attributes_sentence = (
        orig_vertex_symbol
        + out_vertex_attributes_str
        + connection_2
        + avoid_out_vertex_attributes_str
    )

    in_vertex_symbol = (
        f"${alt_orig_vertex_symbol}$"
        if in_vertex_attributes or avoid_in_vertex_attributes
        else ""
    )
    in_vertex_attributes_str = (
        " is " + in_vertex_attributes if in_vertex_attributes else ""
    )
    connection_3 = (
        " and " if in_vertex_attributes and avoid_in_vertex_attributes else ""
    )
    avoid_in_vertex_attributes_str = (
        " is not " + avoid_in_vertex_attributes if avoid_in_vertex_attributes else ""
    )
    in_vertex_attribtues_sentence = (
        in_vertex_symbol
        + in_vertex_attributes_str
        + connection_3
        + avoid_in_vertex_attributes_str
    )

    connection_4 = ""
    if edge_attributes_sentence and out_vertex_attributes_sentence:
        connection_4 = ", where "
    elif out_vertex_attributes_sentence:
        connection_4 = " where "
    connection_5 = ", where " if in_vertex_attribtues_sentence else ""

    return (
        edge_attributes_sentence
        + connection_4
        + out_vertex_attributes_sentence
        + connection_5
        + in_vertex_attribtues_sentence
    )


def build_edge_info_sentence(
    orig_vertex_symbol: str, alt_orig_vertex_symbol: str, row_info: GraphConstructionRow
) -> str:
    """
    Construct an english sentence containing the information pertaining to this row of inputs,
    including what vertices and edges to include or avoid.
    """
    edge = ""
    in_vertex_attributes = ""
    edge_attributes = ""
    avoid_edge_attributes = ""
    avoid_in_vertex_attributes = ""

    if row_info.edge_to_same_vertex_in_G:
        edge = f"${orig_vertex_symbol}$ "
    else:
        edge = (
            f"${orig_vertex_symbol}$ " + r"$\to$" + f" ${alt_orig_vertex_symbol}$ edge"
        )
        edge_attributes = su.list_to_english(row_info.spec_edge_types)
        avoid_edge_attributes = su.list_to_english(row_info.avoid_spec_edge_types)
        in_vertex_attributes = su.list_to_english(row_info.spec_in_vertex_types)
        avoid_in_vertex_attributes = su.list_to_english(
            row_info.avoid_spec_in_vertex_types
        )

    out_vertex_attributes = su.list_to_english(row_info.spec_out_vertex_types)
    avoid_out_vertex_attributes = su.list_to_english(
        row_info.avoid_spec_out_vertex_types
    )

    attributes_info = get_complete_attributes_sentence(
        out_vertex_attributes,
        in_vertex_attributes,
        avoid_out_vertex_attributes,
        avoid_in_vertex_attributes,
        edge_attributes,
        avoid_edge_attributes,
        orig_vertex_symbol,
        alt_orig_vertex_symbol,
    )

    return f"For each {edge} in $G${attributes_info}, $G'$ should contain the edge"


def get_mustache_path(data: QuestionData) -> str:
    return os.path.join(
        data["options"]["server_files_course_path"],
        "theorielearn",
        "graph_construction",
        "graph-construction.mustache",
    )


def generate(
    data: QuestionData,
    rows_info: list[GraphConstructionRow],
    part_symbols: list[str],
    alt_orig_vertex_symbol: str,
) -> None:
    """
    Generates the html for a graph construction question where student inputs vertices to represent edge transitions.

    @param data QuestionData
        Question data dictionary
    @param rows_info List[GraphConstructionRow]
        Contains information on the input rows, such as if it is describing an edge in G with particular attributes like scenic
    @param part_symbols List[str]
        List of all part symbols that edges can go outward from, where the indices, eg. ["u", "a", "b"]
    @param alt_orig_vertex_symbol str
        Alternate part symbol of vertices that edges go inward to on the original graph, e.g. "v", so v and u are distinct
    @return None
    """

    placeholder_1 = "eg. (" + ", ".join(part_symbols) + ")"
    alt_part_symbols = deepcopy(part_symbols)
    alt_part_symbols[0] = alt_orig_vertex_symbol
    usual_placeholder_2 = "eg. (" + ", ".join(alt_part_symbols) + ")"

    # add html input based on information from each row and the submission info at the end.
    with open(
        get_mustache_path(data),
        "r",
        encoding="utf-8",
    ) as f:
        html_params: dict[str, Any] = {"row_input": [], "submit_info": True}
        for i, row_info in enumerate(rows_info):
            # assumes first part is for original vertex.
            attributes_sentence = (
                row_info.alternate_sentence
                if row_info.alternate_sentence
                else build_edge_info_sentence(
                    part_symbols[0], alt_orig_vertex_symbol, row_info
                )
            )
            placeholder_2 = (
                usual_placeholder_2
                if not row_info.edge_to_same_vertex_in_G
                else placeholder_1
            )

            row_params = {
                "attributes_sentence": attributes_sentence,
                "placeholder_1": placeholder_1,
                "answers_name_1": f"ans{2 * i + 1}",
                "correct_answer_1": row_info.correct_answer_outgoing,
                "answers_name_2": f"ans{2 * i + 2}",
                "placeholder_2": placeholder_2,
                "correct_answer_2": row_info.correct_answer_incoming,
            }
            html_params["row_input"].append(row_params)
        data["params"]["html"] = chevron.render(f, html_params).strip()
        data["params"]["inputs_and_info"] = data["params"]["html"]


def get_special_vertices(
    special_vertices: dict[str, set[str]], special_vertex_types: Optional[list[str]]
) -> list[set[str]]:
    if not special_vertex_types:
        return []
    return [
        special_vertices[special_vertex_type]
        for special_vertex_type in special_vertex_types
    ]


def get_special_edges(
    special_edges: dict[str, set[StrEdge]], special_edge_types: Optional[list[str]]
) -> list[set[StrEdge]]:
    if not special_edge_types:
        return []
    return [
        special_edges[special_edge_type] for special_edge_type in special_edge_types
    ]


def generate_new_graph_vertices(part_values: list[set[str]]) -> nx.DiGraph:
    new_graph = nx.DiGraph()
    new_graph.add_nodes_from(
        map(lambda x: str(x).replace("'", ""), product(*part_values))
    )
    return new_graph


def is_vertex_parts_valid(
    v_parts: list[str],
    part_values: list[set[str]],
    part_symbols: list[str],
    alt_orig_vertex_symbol: str,
) -> bool:
    for i, (part_symbol, part_value, v_part) in enumerate(
        zip(part_symbols, part_values, v_parts)
    ):
        valid_values = list(part_value)
        valid_values.append(part_symbol)
        if i == 0:
            # Assumes part corresponding to original vertices in graph G are in first index.
            valid_values.append(alt_orig_vertex_symbol)
        if v_part not in valid_values:
            return False
    return True


def is_describing_vertex(
    v_orig: str, special_vertices: list[set[str]], avoid: bool
) -> bool:
    if not special_vertices:
        return True

    for special_vertex in special_vertices:
        if not avoid and v_orig not in special_vertex:
            return False
        elif avoid and v_orig in special_vertex:
            return False

    return True


def is_describing_edge(
    orig_edge: StrEdge, spec_edges: list[set[StrEdge]], avoid: bool
) -> bool:
    if not spec_edges:
        return True

    for spec_edges_set in spec_edges:
        if not avoid and not any(
            orig_edge == spec_edge for spec_edge in spec_edges_set
        ):
            return False
        elif avoid and any(orig_edge == spec_edge for spec_edge in spec_edges_set):
            return False

    return True


def vertex_and_edge_match_row_info(
    out_v_orig: str,
    in_v_orig: str,
    orig_edge: StrEdge,
    spec_out_vertices: list[set[str]],
    spec_in_vertices: list[set[str]],
    avoid_spec_out_vertices: list[set[str]],
    avoid_spec_in_vertices: list[set[str]],
    spec_edges: list[set[StrEdge]],
    avoid_spec_edges: list[set[StrEdge]],
) -> bool:
    """
    Filter out vertices or edges that the row_info is not descibing.
    """
    if not is_describing_vertex(out_v_orig, spec_out_vertices, avoid=False):
        return False
    elif not is_describing_vertex(in_v_orig, spec_in_vertices, avoid=False):
        return False
    elif not is_describing_vertex(out_v_orig, avoid_spec_out_vertices, avoid=True):
        return False
    elif not is_describing_vertex(in_v_orig, avoid_spec_in_vertices, avoid=True):
        return False
    elif not is_describing_edge(orig_edge, spec_edges, avoid=False):
        return False
    elif not is_describing_edge(orig_edge, avoid_spec_edges, avoid=True):
        return False
    return True


def vertex_pair_part_matches(
    student_out_v_part: str,
    student_in_v_part: str,
    new_graph_out_v_part: str,
    new_graph_in_v_part: str,
    any_symb: str,
) -> bool:
    """
    If the student answer contains the part symbol for both outgoing and incoming vertices, the new_graph outgoing and incoming vertices must match
    Otherwise if the student answer contains the part symbol for either the outgoing or incoming vertices, the other vertex (incoming or outgoing) must match the corresponding new_graph vertex.
    Otherwise, check that the student answer matches the new_graph vertices.
    """
    if (
        student_out_v_part == any_symb
        and student_in_v_part == any_symb
        and new_graph_out_v_part == new_graph_in_v_part
    ):
        return True
    elif student_out_v_part == any_symb and student_in_v_part == new_graph_in_v_part:
        return True
    elif student_in_v_part == any_symb and student_out_v_part == new_graph_out_v_part:
        return True
    elif (
        student_out_v_part == new_graph_out_v_part
        and student_in_v_part == new_graph_in_v_part
    ):
        return True
    return False


def vertex_pair_matches(
    student_out_v: list[str],
    student_in_v: list[str],
    new_graph_out_v: list[str],
    new_graph_in_v: list[str],
    part_symbols: list[str],
    alt_orig_vertex_symbol: str,
) -> bool:
    """
    First check vertices from the set V (original vertices) match.
    Index for the part based on the original vertices is assumed to be 0.
    """
    v_idx = 0
    v_matches = vertex_pair_part_matches(
        student_out_v[v_idx],
        student_in_v[v_idx],
        new_graph_out_v[v_idx],
        new_graph_in_v[v_idx],
        part_symbols[v_idx],
    ) or vertex_pair_part_matches(
        student_out_v[v_idx],
        student_in_v[v_idx],
        new_graph_out_v[v_idx],
        new_graph_in_v[v_idx],
        alt_orig_vertex_symbol,
    )
    if (
        student_out_v[v_idx] == part_symbols[v_idx]
        and student_in_v[v_idx] == alt_orig_vertex_symbol
        and new_graph_out_v[v_idx] != new_graph_in_v[v_idx]
        or student_out_v[v_idx] == alt_orig_vertex_symbol
        and student_in_v[v_idx] == part_symbols[v_idx]
        and new_graph_out_v[v_idx] != new_graph_in_v[v_idx]
    ):
        v_matches = True

    for (
        student_out_v_part,
        student_in_v_part,
        new_graph_out_v_part,
        new_graph_in_v_part,
        part_symbol,
    ) in islice(
        zip(student_out_v, student_in_v, new_graph_out_v, new_graph_in_v, part_symbols),
        1,
        None,
    ):
        if not vertex_pair_part_matches(
            student_out_v_part,
            student_in_v_part,
            new_graph_out_v_part,
            new_graph_in_v_part,
            part_symbol,
        ):
            return False

    return v_matches


def verify_num_of_parts_and_parens(
    part_values: list[set[str]],
    num_out_parts: int,
    num_in_parts: int,
    student_outgoing_v: str,
    student_incoming_v: str,
) -> None:
    """
    Verify that student inputs contain opening and closing brackets, and the same number of parts as defined in the question.
    """
    num_parts = len(part_values)
    if (num_out_parts != num_parts and num_in_parts != num_parts) or (
        (not student_outgoing_v.startswith("(") or not student_outgoing_v.endswith(")"))
        and (
            not student_incoming_v.startswith("(")
            or not student_incoming_v.endswith(")")
        )
    ):
        raise ValueError("Invalid vertex format: outgoing vertex, incoming vertex")
    elif (
        num_out_parts != num_parts
        or not student_outgoing_v.startswith("(")
        or not student_outgoing_v.endswith(")")
    ):
        raise ValueError("Invalid vertex format: outgoing vertex")
    elif (
        num_in_parts != num_parts
        or not student_incoming_v.startswith("(")
        or not student_incoming_v.endswith(")")
    ):
        raise ValueError("Invalid vertex format: incoming vertex")


def verify_has_valid_parts(
    part_values: list[set[str]],
    st_out_v_parts: list[str],
    st_in_v_parts: list[str],
    part_symbols: list[str],
    alt_orig_vertex_symbol: str,
) -> None:
    """
    Verify that each part of the student input uses a defined symbol or value.
    """
    st_out_v_parts_valid = is_vertex_parts_valid(
        st_out_v_parts, part_values, part_symbols, alt_orig_vertex_symbol
    )
    st_in_v_parts_valid = is_vertex_parts_valid(
        st_in_v_parts, part_values, part_symbols, alt_orig_vertex_symbol
    )
    if not st_out_v_parts_valid and not st_in_v_parts_valid:
        raise ValueError("Invalid parts: outgoing vertex, incoming vertex")
    elif not st_out_v_parts_valid:
        raise ValueError("Invalid parts: outgoing vertex")
    elif not st_in_v_parts_valid:
        raise ValueError("Invalid parts: incoming vertex")


def verify_uses_defined_symbols(
    st_out_v_parts: list[str],
    st_in_v_parts: list[str],
    edge_to_same_vertex_in_G: bool,
    alt_orig_vertex_symbol: str,
) -> None:
    """
    Check that student does not use alternate symbol like "v" when only one symbols like "u" is defined.
    Note: this assumes the first part of the new vertex is based on vertices in G.
    """
    if edge_to_same_vertex_in_G:
        if (
            st_out_v_parts[0] == alt_orig_vertex_symbol
            and st_in_v_parts[0] == alt_orig_vertex_symbol
        ):
            raise ValueError(
                "Use of undefined symbol: outgoing vertex, incoming vertex"
            )
        elif st_out_v_parts[0] == alt_orig_vertex_symbol:
            raise ValueError("Use of undefined symbol: outgoing vertex")
        elif st_in_v_parts[0] == alt_orig_vertex_symbol:
            raise ValueError("Use of undefined symbol: incoming vertex")


def parse_submission_and_modify_graph(
    *,
    student_outgoing_v: str,
    student_incoming_v: str,
    student_graph: nx.DiGraph,
    edge_to_same_vertex_in_G: bool,
    original_graph: nx.DiGraph,
    part_values: list[set[str]],
    part_symbols: list[str],
    alt_orig_vertex_symbol: str,
    spec_out_vertices: list[set[str]],
    spec_in_vertices: list[set[str]],
    avoid_spec_out_vertices: list[set[str]],
    avoid_spec_in_vertices: list[set[str]],
    spec_edges: list[set[StrEdge]],
    avoid_spec_edges: list[set[StrEdge]],
    special_row_id: str = None,
) -> nx.DiGraph:
    """
    This parses the student inputs and modifies the new graph G' such that the edge transitions reflect these inputs as feedback.
    """
    generated_graph = student_graph.copy()
    st_out_v_parts = student_outgoing_v.strip("()").replace(" ", "").split(",")
    st_in_v_parts = student_incoming_v.strip("()").replace(" ", "").split(",")

    verify_num_of_parts_and_parens(
        part_values,
        len(st_out_v_parts),
        len(st_in_v_parts),
        student_outgoing_v,
        student_incoming_v,
    )
    verify_has_valid_parts(
        part_values, st_out_v_parts, st_in_v_parts, part_symbols, alt_orig_vertex_symbol
    )
    verify_uses_defined_symbols(
        st_out_v_parts, st_in_v_parts, edge_to_same_vertex_in_G, alt_orig_vertex_symbol
    )

    st_out_v_orig = st_out_v_parts[0]
    st_in_v_orig = st_in_v_parts[0]

    # modify edge transitions based on the outgoing and incoming vertices description.
    student_graph_vertices = deepcopy(generated_graph.nodes)
    for out_vertex_in_vertex in product(student_graph_vertices, student_graph_vertices):
        out_vertex = out_vertex_in_vertex[0]
        in_vertex = out_vertex_in_vertex[1]
        if out_vertex == in_vertex:
            continue

        # filter out candidate vertices based on question parameters.
        out_v_parts = out_vertex.strip('"()').replace(" ", "").split(",")
        in_v_parts = in_vertex.strip('"()').replace(" ", "").split(",")

        # assumes original vertices of G are in the first part.
        out_v_orig = str(out_v_parts[0])
        in_v_orig = str(in_v_parts[0])
        orig_edge = StrEdge(out_v_orig, in_v_orig)
        if out_v_orig != in_v_orig and not original_graph.has_edge(
            out_v_orig, in_v_orig
        ):
            continue
        elif not vertex_and_edge_match_row_info(
            out_v_orig,
            in_v_orig,
            orig_edge,
            spec_out_vertices,
            spec_in_vertices,
            avoid_spec_out_vertices,
            avoid_spec_in_vertices,
            spec_edges,
            avoid_spec_edges,
        ):
            continue

        # create new edge for student's graph.
        if vertex_pair_matches(
            st_out_v_parts,
            st_in_v_parts,
            out_v_parts,
            in_v_parts,
            part_symbols,
            alt_orig_vertex_symbol,
        ):
            if (
                st_out_v_orig == alt_orig_vertex_symbol
                and st_in_v_orig == part_symbols[0]
            ):
                add_edge_to_graph(
                    in_vertex,
                    out_vertex,
                    out_v_orig,
                    in_v_orig,
                    generated_graph,
                    original_graph,
                    special_row_id,
                )
            else:
                add_edge_to_graph(
                    out_vertex,
                    in_vertex,
                    out_v_orig,
                    in_v_orig,
                    generated_graph,
                    original_graph,
                    special_row_id,
                )

    return generated_graph


def add_edge_to_graph(
    out_vertex: str,
    in_vertex: str,
    out_v_orig: str,
    in_v_orig: str,
    generated_graph: nx.DiGraph,
    original_graph: nx.DiGraph,
    special_row_id: str | None,
) -> None:
    generated_graph.add_edge(out_vertex, in_vertex)


def handle_format_error(
    err_str: str,
    str_pattern: str,
    num1: str,
    num2: str,
    feedback_msg: str,
    data: QuestionData,
) -> None:
    if err_str == str_pattern + "outgoing vertex, incoming vertex":
        data["format_errors"]["ans" + num1] = html.escape(feedback_msg)
        data["format_errors"]["ans" + num2] = html.escape(feedback_msg)
    elif err_str == str_pattern + "outgoing vertex":
        data["format_errors"]["ans" + num1] = html.escape(feedback_msg)
    elif err_str == str_pattern + "incoming vertex":
        data["format_errors"]["ans" + num2] = html.escape(feedback_msg)


def grade(
    *,
    data: QuestionData,
    original_graph: nx.DiGraph,
    part_values: list[set[str]],
    part_symbols: list[str],
    alt_orig_vertex_symbol: str,
    special_vertices: dict[str, set[str]],
    special_edges: dict[str, set[StrEdge]],
    rows_info: list[GraphConstructionRow],
    vertical: bool = True,
    has_weights: bool = False,
) -> None:
    """
    Grades student inputs and handles errors. It generates the new graph G' based on student inputs.

    Note: "Part" refers to a section of the new vertex V' which is created through product construction.
    E.g. (1, 2, 9) has 3 parts "1", "2", and "9".

    @param data QuestionData
        Question data dictionary
    @param part_values List[Set[str]]
        List of sets of part values of a vertex, eg. [{"a", "b", "c", "d"}, {"1", "2", "3", "4", "5"}, {"0", "1", "2"}]
    @param part_symbols List[str]
        List of all part symbols that edges can go outward from, where the indices, eg. ["u", "a", "b"]
    @param alt_orig_vertex_symbol str
        Alternate part symbol of vertices that edges go inward to on the original graph, e.g. "v", so the nodes v and u represent are distinct
    @param special_vertices Dict[str, Set[str]]
        List of of dictionaries of special symbols and their corresponding set of values,
        e.g. {"b": {"1", "2", "3"}, "c": {"1", "2"}, "z": {"2"}}
    @param special_edges Dict[str, Set[StrEdge]
        Contains tuples (a, b) representing the edge a -> b, with a string label as the key,
        e.g. {"a": {StrEdge obj, StrEdge obj}, "b": {StrEdge obj, StrEdge obj}, "n": {StrEdge obj}}, where StrEdge obj is an object of the StrEdge class
    @param rows_info: List[GraphConstructionRow]
        Contains information on the input rows, such as if it is describing an edge in G with particular attributes like scenic
    @param horizontal bool
        Displays the graph as horizontal or vertical
    @return None
    """

    # generate new feedback graph.
    student_graph = generate_new_graph_vertices(part_values)

    for i, row_info in enumerate(rows_info):
        num1 = str(2 * i + 1)
        num2 = str(2 * i + 2)
        student_outgoing_v = data["submitted_answers"]["ans" + num1]
        student_incoming_v = data["submitted_answers"]["ans" + num2]
        try:
            # Get special vertices and edges that pertain to the row.
            spec_out_vertices = get_special_vertices(
                special_vertices, row_info.spec_out_vertex_types
            )
            spec_in_vertices = get_special_vertices(
                special_vertices, row_info.spec_in_vertex_types
            )
            avoid_spec_out_vertices = get_special_vertices(
                special_vertices, row_info.avoid_spec_out_vertex_types
            )
            avoid_spec_in_vertices = get_special_vertices(
                special_vertices, row_info.avoid_spec_in_vertex_types
            )

            spec_edges = get_special_edges(special_edges, row_info.spec_edge_types)
            avoid_spec_edges = get_special_edges(
                special_edges, row_info.avoid_spec_edge_types
            )

            student_graph = parse_submission_and_modify_graph(
                student_outgoing_v=student_outgoing_v,
                student_incoming_v=student_incoming_v,
                student_graph=student_graph,
                edge_to_same_vertex_in_G=row_info.edge_to_same_vertex_in_G,
                original_graph=original_graph,
                part_values=part_values,
                part_symbols=part_symbols,
                alt_orig_vertex_symbol=alt_orig_vertex_symbol,
                spec_out_vertices=spec_out_vertices,
                spec_in_vertices=spec_in_vertices,
                avoid_spec_out_vertices=avoid_spec_out_vertices,
                avoid_spec_in_vertices=avoid_spec_in_vertices,
                spec_edges=spec_edges,
                avoid_spec_edges=avoid_spec_edges,
                special_row_id=row_info.special_row_id,
            )
        except ValueError as err:
            err_str = str(err)
            format_feedback_msg = "Please format your vertex definition with the required parts, consistent with your definition in the previous question, and with parentheses."
            handle_format_error(
                err_str,
                "Invalid vertex format: ",
                num1,
                num2,
                format_feedback_msg,
                data,
            )

            parts_feedback_msg = "Your vertex definition does not match any vertex in G'. Please check that you are using only valid symbols as described in the beginning."
            handle_format_error(
                err_str, "Invalid parts: ", num1, num2, parts_feedback_msg, data
            )

            # Only pertains to the inputs in which only the main symbol is defined, e.g. only u is defined, not u and v. Used for cases such as (u, a, b) -> (u, c, d).
            invalid_symb_mgs = f'Use of undefined symbol "{alt_orig_vertex_symbol}". Remember only "{part_symbols[0]}" is defined here.'
            handle_format_error(
                err_str, "Use of undefined symbol: ", num1, num2, invalid_symb_mgs, data
            )

    combined_graphs = nx.union(original_graph, student_graph)
    rankdir = "TB" if vertical else "LR"
    html_params = {
        "inputs_and_info": data["params"]["inputs_and_info"],
        "feedback_pl_graph": {
            "combined_graphs": generate_pl_graph(
                combined_graphs, rankdir=rankdir, label="label"
            )
        },
    }
    with open(
        get_mustache_path(data),
        "r",
        encoding="utf-8",
    ) as f:
        data["params"]["html"] = chevron.render(f, html_params)
