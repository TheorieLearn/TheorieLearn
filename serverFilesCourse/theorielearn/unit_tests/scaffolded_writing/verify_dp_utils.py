import theorielearn.scaffolded_writing.dp_utils as sw_du
from theorielearn.scaffolded_writing.dp_cfgs import get_partition_sum_cfg


class VerifyDPStudentSubmission:
    def verify_func_name_and_params(self) -> None:
        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "the subproblem",
                "to be the",
                "number of terms",
                "that can be obtained",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        assert submission.func_name is None
        assert submission.func_params == set()

        submission = sw_du.DPStudentSubmission(
            ["define", "DP(i)", "to be the", "sum", "that can be obtained", "."],
            get_partition_sum_cfg(),
        )
        assert submission.func_name == "DP"
        assert submission.func_params == {"i"}

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "MaxSum(i,j)",
                "to be the",
                "answer",
                "that can be obtained",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        assert submission.func_name == "MaxSum"
        assert submission.func_params == {"i", "j"}

    def verify_mentioned_variables(self) -> None:
        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        assert submission.mentioned_variables == set()

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[1..i]",
                "using",
                "at most",
                "t",
                "2-digit terms",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        assert submission.mentioned_variables == {"i", "t"}

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[1..n]",
                "under the constraint that",
                "A[1]",
                "is part of a",
                "j-digit",
                "term",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        assert submission.mentioned_variables == {"n", "j"}


class VerifyDPConstraints:
    def verify_declare_function_constraint(self) -> None:
        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "the subproblem",
                "to be the",
                "answer",
                "that can be obtained",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        constraint = sw_du.declare_func_constraint()
        assert constraint(submission)

        submission = sw_du.DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "answer", "that can be obtained", "."],
            get_partition_sum_cfg(),
        )
        constraint = sw_du.declare_func_constraint()
        assert not constraint(submission)

    def verify_output_noun_and_adj_constraint(self) -> None:
        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "the subproblem",
                "to be the",
                "answer",
                "that can be obtained",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        constraint = sw_du.correct_noun_and_adj_constraint("sum", "maximum")
        feedback = constraint(submission)
        assert feedback
        assert '"answer" is too vague' in feedback

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "the subproblem",
                "to be the",
                "number of terms",
                "that can be obtained",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        constraint = sw_du.correct_noun_and_adj_constraint("sum", "maximum")
        feedback = constraint(submission)
        assert feedback
        assert "not directly relevant" in feedback

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "the subproblem",
                "to be the",
                "sum",
                "that can be obtained",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        constraint = sw_du.correct_noun_and_adj_constraint("sum", "maximum")
        feedback = constraint(submission)
        assert feedback
        assert 'add an adjective in front of "sum"' in feedback

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "the subproblem",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        constraint = sw_du.correct_noun_and_adj_constraint("sum", "minimum")
        feedback = constraint(submission)
        assert feedback
        assert "not directly relevant" in feedback

        constraint = sw_du.correct_noun_and_adj_constraint("sum", "maximum")
        assert not constraint(submission)

    def verify_descriptive_function_name(self) -> None:
        submission = sw_du.DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "answer", "that can be obtained", "."],
            get_partition_sum_cfg(),
        )
        constraint = sw_du.descriptive_func_name_constraint("MinSum")
        assert constraint(submission)

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "MinSum(i,j)",
                "to be the",
                "answer",
                "that can be obtained",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        constraint = sw_du.descriptive_func_name_constraint("MinSum")
        assert not constraint(submission)

    def verify_explain_params_constraint(self) -> None:
        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..n]",
                "using",
                "at most",
                "t",
                "2-digit terms",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        constraint = sw_du.explain_params_constraint(variables_in_problem={"n"})
        feedback = constraint(submission)
        assert feedback
        assert "takes j as" in feedback

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "for i and j",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        constraint = sw_du.explain_params_constraint(variables_in_problem={"n", "t"})
        feedback = constraint(submission)
        assert feedback
        assert "mentions the function's input parameters" in feedback

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..n]",
                "using",
                "at most",
                "t",
                "2-digit terms",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        constraint = sw_du.explain_params_constraint(variables_in_problem={"n", "t"})
        assert not constraint(submission)

    def verify_decoupled_parameters_constraint(self) -> None:
        constraint = sw_du.decoupled_parameters_constraint(
            SUBARRAY="an array index",
            COMPARISON_RHS="the number of 2-digit terms",
            TERM_LENGTH="a term length",
        )

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..n]",
                "under the constraint that",
                "A[1]",
                "is part of a",
                "i-digit",
                "term",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        feedback = constraint(submission)
        assert feedback
        assert (
            feedback
            == "You used the parameter i to denote both an array index and a term length. It doesn't make sense to tie both of these quantities to the same parameter because these quantities can vary independently."
        )

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..j]",
                "using",
                "at most",
                "j",
                "2-digit terms",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        feedback = constraint(submission)
        assert feedback
        assert (
            feedback
            == "You used the parameter j to denote both an array index and the number of 2-digit terms. It doesn't make sense to tie both of these quantities to the same parameter because these quantities can vary independently."
        )

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..n]",
                "under the constraint that",
                "A[i]",
                "is part of a",
                "j-digit",
                "term",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        feedback = constraint(submission)
        assert not feedback

    def verify_can_compute_final_answer_constraint(self) -> None:
        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..n]",
                "under the constraint that",
                "A[1]",
                "is part of a",
                "j-digit",
                "term",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        constraint = sw_du.can_compute_final_answer_constraint(
            "NUM_TWO_DIGIT_TERMS_RESTRICTION",
            "COMPARISON_OPERATOR",
            "VIABLE_COMPARISON_OPERATOR",
            feedback_elaboration="at most t 2-digit terms are used",
        )
        feedback = constraint(submission)
        assert feedback
        assert (
            feedback
            == "Your subproblem definition does not allow us to compute the final answer requested by the original problem. The problem requires that at most t 2-digit terms are used, but there is no way to impose this requirement using your subproblem definition."
        )

        # check that comparison operator is taken into account
        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..n]",
                "using",
                "at least",
                "t",
                "2-digit terms",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        assert constraint(submission)

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..n]",
                "using",
                "at most",
                "t",
                "2-digit terms",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        assert not constraint(submission)

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..n]",
                "using",
                "exactly",
                "t",
                "2-digit terms",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        assert not constraint(submission)

    def verify_reduces_recursively_constraint(self) -> None:
        def get_unhandled_scenario(submission: sw_du.DPStudentSubmission) -> str:
            return "if we decide to make the last term 2 digits, then we would need to call a subproblem that analyzes the subarray A[1..n-2]"

        constraint = sw_du.reduces_recursively_constraint(
            "SUBARRAY", get_unhandled_scenario
        )

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[1..n]",
                "under the constraint that",
                "A[1]",
                "is part of a",
                "j-digit",
                "term",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        feedback = constraint(submission)
        assert feedback
        assert (
            feedback
            == "Make sure that your subproblem can be reduced to smaller instances of itself. For example, if we decide to make the last term 2 digits, then we would need to call a subproblem that analyzes the subarray A[1..n-2], but your subproblem definition does not allow us to do that."
        )

        # Check that it still works if the SUBARRAY field is missing entirely
        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "under the constraint that",
                "A[1]",
                "is part of a",
                "j-digit",
                "term",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        feedback = constraint(submission)
        assert feedback
        assert (
            feedback
            == "Make sure that your subproblem can be reduced to smaller instances of itself. For example, if we decide to make the last term 2 digits, then we would need to call a subproblem that analyzes the subarray A[1..n-2], but your subproblem definition does not allow us to do that."
        )

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..n]",
                "using",
                "at most",
                "t",
                "2-digit terms",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        assert not constraint(submission)

    def verify_no_irrelevant_restrictions_constraint(self) -> None:
        constraint = sw_du.no_irrelevant_restrictions_constraint(
            "FIRST_OR_LAST_TERM_RESTRICTION"
        )

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..n]",
                "under the constraint that",
                "A[1]",
                "is part of a",
                "j-digit",
                "term",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        assert constraint(submission)

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..n]",
                "using",
                "at most",
                "t",
                "2-digit terms",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        assert not constraint(submission)

    def verify_no_double_ended_parameterization_constraint(self) -> None:
        constraint = sw_du.no_double_ended_parameterization_constraint()

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..j]",
                "under the constraint that",
                "A[1]",
                "is part of a",
                "j-digit",
                "term",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        assert constraint(submission)

        submission = sw_du.DPStudentSubmission(
            [
                "define",
                "DP(i,j)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..n]",
                "using",
                "at most",
                "t",
                "2-digit terms",
                ".",
            ],
            get_partition_sum_cfg(),
        )
        assert not constraint(submission)


class VerifyMiscellaneousUtils:
    def verify_concat_into_production_rule(self) -> None:
        assert (
            sw_du.concat_into_production_rule(["DP", "MaxSum"], ["(i)", "(i,j)"])
            == '"DP(i)" | "DP(i,j)" | "MaxSum(i)" | "MaxSum(i,j)"'
        )
