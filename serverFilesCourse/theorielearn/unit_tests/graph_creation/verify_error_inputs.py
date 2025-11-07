import theorielearn.graph_construction.server_base as server_base
import pytest


class VerifyInputErrors:
    @pytest.mark.parametrize(
        "part_values, num_out_parts, num_in_parts, student_outgoing_v, student_incoming_v",
        [
            (
                [{"a", "b", "c"}, {"d", "e"}, {"f", "g"}],
                4,
                3,
                "(1, 2, 3, 4)",
                "(1, 2, 3)",
            ),
            ([{"a", "b", "c"}, {"d", "e"}, {"f", "g"}], 3, 3, "1, 2, 3)", "(1, 2, 3)"),
            ([{"a", "b", "c"}, {"d", "e"}, {"f", "g"}], 3, 3, "(1, 2, 3", "(1, 2, 3)"),
            (
                [{"a", "b", "c"}, {"d", "e"}, {"f", "g"}],
                3,
                3,
                "(1, 2, 3)x",
                "(1, 2, 3)",
            ),
            (
                [{"a", "b", "c"}, {"d", "e"}, {"f", "g"}],
                3,
                4,
                "(1, 2, 3, 4)",
                "(1, 2, 3)",
            ),
            ([{"a", "b", "c"}, {"d", "e"}, {"f", "g"}], 3, 3, "(1, 2, 3)", "1, 2, 3)"),
            ([{"a", "b", "c"}, {"d", "e"}, {"f", "g"}], 3, 3, "(1, 2, 3)", "(1, 2, 3"),
            (
                [{"a", "b", "c"}, {"d", "e"}, {"f", "g"}],
                3,
                3,
                "(1, 2, 3)",
                "(1, 2, 3)x",
            ),
        ],
    )
    def verify_incorrect_num_of_parts_and_parens(
        self,
        part_values: list[set[str]],
        num_out_parts: int,
        num_in_parts: int,
        student_outgoing_v: str,
        student_incoming_v: str,
    ) -> None:
        with pytest.raises(ValueError):
            server_base.verify_num_of_parts_and_parens(
                part_values,
                num_out_parts,
                num_in_parts,
                student_outgoing_v,
                student_incoming_v,
            )

    @pytest.mark.parametrize(
        "part_values, num_out_parts, num_in_parts, student_outgoing_v, student_incoming_v",
        [([{"a", "b", "c"}, {"d", "e"}, {"f", "g"}], 3, 3, "(1, 2, 3)", "(1, 2, 3)")],
    )
    def verify_correct_num_of_parts_and_parens(
        self,
        part_values: list[set[str]],
        num_out_parts: int,
        num_in_parts: int,
        student_outgoing_v: str,
        student_incoming_v: str,
    ) -> None:
        try:
            server_base.verify_num_of_parts_and_parens(
                part_values,
                num_out_parts,
                num_in_parts,
                student_outgoing_v,
                student_incoming_v,
            )
        except Exception:
            assert False, "verify_num_of_parts_and_perens raised an exception when it should not have."

    @pytest.mark.parametrize(
        "part_values, st_out_v_parts, st_in_v_parts, part_symbols, alt_orig_vertex_symbol",
        [
            (
                [{"a", "b", "c"}, {"d", "e"}, {"f", "g"}],
                ["a", "x", "f"],
                ["a", "d", "f"],
                ["u", "D", "F"],
                "v",
            ),
            (
                [{"a", "b", "c"}, {"d", "e"}, {"f", "g"}],
                ["a", "d", "f"],
                ["a", "x", "f"],
                ["u", "D", "F"],
                "v",
            ),
            (
                [{"a", "b", "c"}, {"d", "e"}, {"f", "g"}],
                ["a", "x", "f"],
                ["a", "x", "f"],
                ["u", "D", "F"],
                "v",
            ),
        ],
    )
    def verify_incorrect_has_valid_parts(
        self,
        part_values: list[set[str]],
        st_out_v_parts: list[str],
        st_in_v_parts: list[str],
        part_symbols: list[str],
        alt_orig_vertex_symbol: str,
    ) -> None:
        with pytest.raises(ValueError):
            server_base.verify_has_valid_parts(
                part_values,
                st_out_v_parts,
                st_in_v_parts,
                part_symbols,
                alt_orig_vertex_symbol,
            )

    @pytest.mark.parametrize(
        "part_values, st_out_v_parts, st_in_v_parts, part_symbols, alt_orig_vertex_symbol",
        [
            (
                [{"a", "b", "c"}, {"d", "e"}, {"f", "g"}],
                ["a", "d", "f"],
                ["a", "d", "f"],
                ["u", "D", "F"],
                "v",
            ),
            (
                [{"a", "b", "c"}, {"d", "e"}, {"f", "g"}],
                ["u", "d", "f"],
                ["v", "d", "f"],
                ["u", "D", "F"],
                "v",
            ),
            (
                [{"a", "b", "c"}, {"d", "e"}, {"f", "g"}],
                ["u", "D", "F"],
                ["a", "d", "f"],
                ["u", "D", "F"],
                "v",
            ),
            (
                [{"a", "b", "c"}, {"d", "e"}, {"f", "g"}],
                ["v", "d", "f"],
                ["u", "d", "f"],
                ["u", "D", "F"],
                "v",
            ),
        ],
    )
    def verify_correct_has_valid_parts(
        self,
        part_values: list[set[str]],
        st_out_v_parts: list[str],
        st_in_v_parts: list[str],
        part_symbols: list[str],
        alt_orig_vertex_symbol: str,
    ) -> None:
        try:
            server_base.verify_has_valid_parts(
                part_values,
                st_out_v_parts,
                st_in_v_parts,
                part_symbols,
                alt_orig_vertex_symbol,
            )
        except Exception:
            assert (
                False
            ), "verify_has_valid_parts raised an exception when it should not have."

    @pytest.mark.parametrize(
        "st_out_v_parts, st_in_v_parts, edge_to_same_vertex_in_G, alt_orig_vertex_symbol",
        [
            (["v", "b", "c"], ["a", "b", "c"], True, "v"),
            (["a", "b", "c"], ["v", "b", "c"], True, "v"),
            (["v", "b", "c"], ["v", "b", "c"], True, "v"),
        ],
    )
    def verify_incorrect_uses_defined_symbols(
        self,
        st_out_v_parts: list[str],
        st_in_v_parts: list[str],
        edge_to_same_vertex_in_G: bool,
        alt_orig_vertex_symbol: str,
    ) -> None:
        with pytest.raises(ValueError):
            server_base.verify_uses_defined_symbols(
                st_out_v_parts,
                st_in_v_parts,
                edge_to_same_vertex_in_G,
                alt_orig_vertex_symbol,
            )

    @pytest.mark.parametrize(
        "st_out_v_parts, st_in_v_parts, edge_to_same_vertex_in_G, alt_orig_vertex_symbol",
        [
            (["v", "b", "c"], ["a", "b", "c"], False, "v"),
            (["a", "b", "c"], ["v", "b", "c"], False, "v"),
            (["v", "b", "c"], ["v", "b", "c"], False, "v"),
            (["a", "b", "c"], ["a", "b", "c"], True, "v"),
        ],
    )
    def verify_correct_uses_defined_symbols(
        self,
        st_out_v_parts: list[str],
        st_in_v_parts: list[str],
        edge_to_same_vertex_in_G: bool,
        alt_orig_vertex_symbol: str,
    ) -> None:
        try:
            server_base.verify_uses_defined_symbols(
                st_out_v_parts,
                st_in_v_parts,
                edge_to_same_vertex_in_G,
                alt_orig_vertex_symbol,
            )
        except Exception:
            assert False, "verify_uses_defined_symbols raised an exception when it should not have."
