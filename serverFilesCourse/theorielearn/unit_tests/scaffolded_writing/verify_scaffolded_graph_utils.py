# import pytest
import theorielearn.scaffolded_writing.scaffolded_graph_utils as sw_gu
from theorielearn.scaffolded_writing.graph_cfgs import get_french_flag_cfg


class VerifyGraphConstraints:
    def verify_used_both_graphs(self) -> None:
        submission = sw_gu.GraphStudentSubmission(
            ["the graph G has a", "cycle", "."], get_french_flag_cfg()
        )

        feedback = sw_gu.used_both_graphs(submission)
        assert feedback
        assert "output" in feedback

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "cycle", "."], get_french_flag_cfg()
        )

        feedback = sw_gu.used_both_graphs(submission)
        assert feedback
        assert "input" in feedback

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "cycle", "and", "the graph G has a", "cycle", "."],
            get_french_flag_cfg(),
        )

        assert not sw_gu.used_both_graphs(submission)

    def verify_used_iff_structre(self) -> None:
        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "cycle", "and", "the graph G has a", "cycle", "."],
            get_french_flag_cfg(),
        )

        assert sw_gu.used_iff_structure(submission)

        submission = sw_gu.GraphStudentSubmission(
            [
                "the graph G' has a",
                "cycle",
                "if and only if",
                "the graph G has a",
                "cycle",
                ".",
            ],
            get_french_flag_cfg(),
        )

        assert not sw_gu.used_iff_structure(submission)

    def verify_correct_object(self) -> None:
        constraint = sw_gu.correct_object({"cycle", "path"})

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G has a", "walk", "."], get_french_flag_cfg()
        )
        assert constraint(submission)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G has a", "path", "."], get_french_flag_cfg()
        )
        assert not constraint(submission)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G has a", "cycle", "."], get_french_flag_cfg()
        )
        assert not constraint(submission)

        constraint = sw_gu.correct_object({"cycle", "path"}, isGprime=True)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "walk", "."], get_french_flag_cfg()
        )
        assert constraint(submission)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "path", "."], get_french_flag_cfg()
        )
        assert not constraint(submission)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "cycle", "."], get_french_flag_cfg()
        )
        assert not constraint(submission)

    def verify_defined_starting_location(self) -> None:
        constraint = sw_gu.defined_starting_location("walk")

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G has a", "walk", "."], get_french_flag_cfg()
        )
        assert constraint(submission)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G has a", "walk", "starting from", "s", "to", "t", "."],
            get_french_flag_cfg(),
        )
        assert not constraint(submission)

        constraint = sw_gu.defined_starting_location("walk", isGprime=True)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "walk", "."], get_french_flag_cfg()
        )
        assert constraint(submission)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "walk", "starting from", "s", "to", "t", "."],
            get_french_flag_cfg(),
        )
        assert not constraint(submission)

    def verify_defined_simple_terminal_node(self) -> None:
        constraint = sw_gu.defined_simple_terminal_node("s", feedback="extra")
        submission = sw_gu.GraphStudentSubmission(
            ["the graph G has a", "walk", "starting from", "(s, 0)", "to", "t", "."],
            get_french_flag_cfg(),
        )
        feedback = constraint(submission)
        assert feedback
        assert "extra" in feedback

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G has a", "walk", "starting from", "s", "to", "t", "."],
            get_french_flag_cfg(),
        )

        constraint = sw_gu.defined_simple_terminal_node("t", isEnd=True)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G has a", "walk", "starting from", "s", "to", "(t, 0)", "."],
            get_french_flag_cfg(),
        )

        assert constraint(submission)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G has a", "walk", "starting from", "s", "to", "t", "."],
            get_french_flag_cfg(),
        )

        assert not constraint(submission)

        constraint = sw_gu.defined_simple_terminal_node(
            "s", isGprime=True, feedback="extra"
        )
        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "walk", "starting from", "(s, 0)", "to", "t", "."],
            get_french_flag_cfg(),
        )
        feedback = constraint(submission)
        assert feedback
        assert "extra" in feedback

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "walk", "starting from", "s", "to", "t", "."],
            get_french_flag_cfg(),
        )

        constraint = sw_gu.defined_simple_terminal_node("t", isGprime=True, isEnd=True)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "walk", "starting from", "s", "to", "(t, 0)", "."],
            get_french_flag_cfg(),
        )

        assert constraint(submission)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "walk", "starting from", "s", "to", "t", "."],
            get_french_flag_cfg(),
        )

        assert not constraint(submission)

    def verify_defined_general_terminal_node(self) -> None:
        constraint = sw_gu.defined_general_terminal_node()

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G has a", "walk", "starting from", "s", "to", "t", "."],
            get_french_flag_cfg(),
        )

        assert constraint(submission)

        submission = sw_gu.GraphStudentSubmission(
            [
                "the graph G has a",
                "walk",
                "starting from",
                "(s,i)",
                "where i is",
                "0",
                "to",
                "t",
                ".",
            ],
            get_french_flag_cfg(),
        )

        assert not constraint(submission)

        constraint = sw_gu.defined_general_terminal_node(isEnd=True)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G has a", "walk", "starting from", "s", "to", "t", "."],
            get_french_flag_cfg(),
        )

        assert constraint(submission)

        submission = sw_gu.GraphStudentSubmission(
            [
                "the graph G has a",
                "walk",
                "starting from",
                "s",
                "to",
                "(t,i)",
                "where i is",
                "0",
                ".",
            ],
            get_french_flag_cfg(),
        )

        assert not constraint(submission)

        constraint = sw_gu.defined_general_terminal_node(isGprime=True)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "walk", "starting from", "s", "to", "t", "."],
            get_french_flag_cfg(),
        )

        assert constraint(submission)

        submission = sw_gu.GraphStudentSubmission(
            [
                "the graph G' has a",
                "walk",
                "starting from",
                "(s,i)",
                "where i is",
                "0",
                "to",
                "t",
                ".",
            ],
            get_french_flag_cfg(),
        )

        assert not constraint(submission)

        constraint = sw_gu.defined_general_terminal_node(isEnd=True, isGprime=True)

        submission = sw_gu.GraphStudentSubmission(
            ["the graph G' has a", "walk", "starting from", "s", "to", "t", "."],
            get_french_flag_cfg(),
        )

        assert constraint(submission)

        submission = sw_gu.GraphStudentSubmission(
            [
                "the graph G' has a",
                "walk",
                "starting from",
                "s",
                "to",
                "(t,i)",
                "where i is",
                "0",
                ".",
            ],
            get_french_flag_cfg(),
        )

        assert not constraint(submission)
