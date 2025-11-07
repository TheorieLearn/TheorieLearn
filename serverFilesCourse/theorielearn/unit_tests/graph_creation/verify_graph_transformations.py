import theorielearn.graph_construction.server_base as server_base
import networkx as nx
import pytest
from theorielearn.graph_construction.server_base import StrEdge


class VerifyGraphTransformations:
    default_original_graph = nx.DiGraph()
    default_original_graph.add_edge("a", "b")
    default_original_graph.add_edge("b", "c")
    default_original_graph = default_original_graph

    default_student_graph = nx.DiGraph()
    default_student_graph.add_node("(a, 1)")
    default_student_graph.add_node("(a, 2)")
    default_student_graph.add_node("(b, 1)")
    default_student_graph.add_node("(b, 2)")
    default_student_graph.add_node("(c, 1)")
    default_student_graph.add_node("(c, 2)")
    default_student_graph = default_student_graph

    default_part_values = [{"a", "b", "c"}, {"1", "2"}]
    default_part_symbols = ["A", "N"]
    default_alt_orig_vertex_symbol = "Z"

    @pytest.mark.parametrize(
        "student_outgoing_v, student_incoming_v, edge_to_same_vertex_in_G, spec_out_vertices, spec_in_vertices, avoid_spec_out_vertices, avoid_spec_in_vertices, spec_edges, avoid_spec_edges, expected_edges",
        [
            ("(a, 1)", "(a, 2)", True, [], [], [], [], [], [], [("(a, 1)", "(a, 2)")]),
            (
                "(A, 1)",
                "(A, 2)",
                True,
                [],
                [],
                [],
                [],
                [],
                [],
                [("(a, 1)", "(a, 2)"), ("(b, 1)", "(b, 2)"), ("(c, 1)", "(c, 2)")],
            ),
            (
                "(A, 1)",
                "(Z, 1)",
                False,
                [],
                [],
                [],
                [],
                [],
                [],
                [("(a, 1)", "(b, 1)"), ("(b, 1)", "(c, 1)")],
            ),
            ("(a, 1)", "(b, 2)", False, [], [], [], [], [], [], [("(a, 1)", "(b, 2)")]),
            ("(a, 1)", "(a, 1)", True, [], [], [], [], [], [], []),  # no self loops,
            (
                "(Z, 1)",
                "(A, 1)",
                False,
                [],
                [],
                [],
                [],
                [],
                [],
                [("(b, 1)", "(a, 1)"), ("(c, 1)", "(b, 1)")],
            ),
            (
                "(A, 1)",
                "(Z, 1)",
                False,
                [{"a"}],
                [{"b"}],
                [],
                [],
                [],
                [],
                [("(a, 1)", "(b, 1)")],
            ),
            (
                "(A, 1)",
                "(Z, 1)",
                False,
                [],
                [],
                [{"a"}],
                [],
                [],
                [],
                [("(b, 1)", "(c, 1)")],
            ),
            (
                "(A, 1)",
                "(Z, 1)",
                False,
                [],
                [],
                [],
                [{"b"}],
                [],
                [],
                [("(b, 1)", "(c, 1)")],
            ),
            (
                "(A, 1)",
                "(Z, 2)",
                False,
                [],
                [],
                [],
                [],
                [{StrEdge("b", "c")}],
                [],
                [("(b, 1)", "(c, 2)")],
            ),
            (
                "(A, 1)",
                "(Z, 2)",
                False,
                [],
                [],
                [],
                [],
                [],
                [{StrEdge("b", "c")}],
                [("(a, 1)", "(b, 2)")],
            ),
            (
                "(A, 1)",
                "(Z, 2)",
                False,
                [],
                [],
                [],
                [],
                [],
                [{StrEdge("b", "c")}, {StrEdge("a", "b")}],
                [],
            ),
        ],
    )
    def verify_incorrect_num_of_parts_and_parens(
        self,
        student_outgoing_v: str,
        student_incoming_v: str,
        edge_to_same_vertex_in_G: bool,
        spec_out_vertices: list[set[str]],
        spec_in_vertices: list[set[str]],
        avoid_spec_out_vertices: list[set[str]],
        avoid_spec_in_vertices: list[set[str]],
        spec_edges: list[set[StrEdge]],
        avoid_spec_edges: list[set[StrEdge]],
        expected_edges: list[tuple[str]],
    ) -> None:
        student_graph = self.default_student_graph.copy()
        student_graph = server_base.parse_submission_and_modify_graph(
            student_outgoing_v=student_outgoing_v,
            student_incoming_v=student_incoming_v,
            student_graph=student_graph,
            edge_to_same_vertex_in_G=edge_to_same_vertex_in_G,
            original_graph=self.default_original_graph,
            part_values=self.default_part_values,
            part_symbols=self.default_part_symbols,
            alt_orig_vertex_symbol=self.default_alt_orig_vertex_symbol,
            spec_out_vertices=spec_out_vertices,
            spec_in_vertices=spec_in_vertices,
            avoid_spec_out_vertices=avoid_spec_out_vertices,
            avoid_spec_in_vertices=avoid_spec_in_vertices,
            spec_edges=spec_edges,
            avoid_spec_edges=avoid_spec_edges,
        )

        assert len(student_graph.edges) == len(expected_edges)

        for edge in student_graph.edges:
            assert edge in expected_edges
