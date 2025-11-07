from theorielearn.scaffolded_writing.cfg import ScaffoldedWritingCFG
from theorielearn.scaffolded_writing.dp_utils import concat_into_production_rule


def get_partition_min_sum_cfg() -> ScaffoldedWritingCFG:
    function_names = concat_into_production_rule(
        ["DP", "Memo", "MinSum", "MaxSum", "MinTerms", "MaxTerms"], ["(i)", "(i,j)"]
    )

    return ScaffoldedWritingCFG.fromstring(
        f"""
        START -> "define" FUNCTION_DECLARATION "to be the" FUNCTION_OUTPUT "."

        FUNCTION_DECLARATION -> "the subproblem" | {function_names}

        FUNCTION_OUTPUT -> EXTREMAL_ADJ OUTPUT_NOUN "that can be obtained" SITUATION

        EXTREMAL_ADJ -> EPSILON | "minimum" | "maximum"
        OUTPUT_NOUN -> "answer" | "number of terms" | "sum"
        SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING | SUBARRAY_RESTRICTION ADDITIONAL_RESTRICTION

        MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j"

        SUBARRAY_RESTRICTION -> EPSILON | "from" SUBARRAY
        SUBARRAY -> "the rest of the array" | "A[1..n]" | PREFIX_SUBPROBLEM | SUFFIX_SUBPROBLEM | DOUBLE_ENDED_SUBPROBLEM
        PREFIX_SUBPROBLEM -> "A[1..i]"
        SUFFIX_SUBPROBLEM -> "A[i..n]"
        DOUBLE_ENDED_SUBPROBLEM -> "A[i..j]"

        ADDITIONAL_RESTRICTION -> EPSILON | NUM_ONE_DIGIT_TERMS_RESTRICTION | FIRST_OR_LAST_TERM_RESTRICTION \
                                | NUM_ONE_DIGIT_TERMS_RESTRICTION "and" FIRST_OR_LAST_TERM_RESTRICTION

        NUM_ONE_DIGIT_TERMS_RESTRICTION -> "using" COMPARISON_OPERATOR COMPARISON_RHS "1-digit terms"
        COMPARISON_OPERATOR -> "at least" | VIABLE_COMPARISON_OPERATOR
        VIABLE_COMPARISON_OPERATOR -> "at most" | "exactly"
        COMPARISON_RHS -> "t" | "i" | "j"

        FIRST_OR_LAST_TERM_RESTRICTION -> "under the constraint that" RESTRICTED_TERM_INDEX "is part of a" TERM_LENGTH "term"
        RESTRICTED_TERM_INDEX -> "A[1]" | "A[n]" | "A[i]"
        TERM_LENGTH -> "1-digit" | "2-digit" | "3-digit" | "i-digit" | "j-digit"

        EPSILON ->
    """
    )

def get_partition_sum_cfg() -> ScaffoldedWritingCFG:
    function_names = concat_into_production_rule(
        ["DP", "Memo", "MinSum", "MaxSum", "MinTerms", "MaxTerms"], ["(i)", "(i,j)"]
    )

    return ScaffoldedWritingCFG.fromstring(
        f"""
        START -> "define" FUNCTION_DECLARATION "to be the" FUNCTION_OUTPUT "."

        FUNCTION_DECLARATION -> "the subproblem" | {function_names}

        FUNCTION_OUTPUT -> EXTREMAL_ADJ OUTPUT_NOUN "that can be obtained" SITUATION

        EXTREMAL_ADJ -> EPSILON | "minimum" | "maximum"
        OUTPUT_NOUN -> "answer" | "number of terms" | "sum"
        SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING | SUBARRAY_RESTRICTION ADDITIONAL_RESTRICTION

        MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j"

        SUBARRAY_RESTRICTION -> EPSILON | "from" SUBARRAY
        SUBARRAY -> "the rest of the array" | "A[1..n]" | PREFIX_SUBPROBLEM | SUFFIX_SUBPROBLEM | DOUBLE_ENDED_SUBPROBLEM
        PREFIX_SUBPROBLEM -> "A[1..i]"
        SUFFIX_SUBPROBLEM -> "A[i..n]"
        DOUBLE_ENDED_SUBPROBLEM -> "A[i..j]"

        ADDITIONAL_RESTRICTION -> EPSILON | NUM_TWO_DIGIT_TERMS_RESTRICTION | FIRST_OR_LAST_TERM_RESTRICTION \
                                | NUM_TWO_DIGIT_TERMS_RESTRICTION "and" FIRST_OR_LAST_TERM_RESTRICTION

        NUM_TWO_DIGIT_TERMS_RESTRICTION -> "using" COMPARISON_OPERATOR COMPARISON_RHS "2-digit terms"
        COMPARISON_OPERATOR -> "at least" | VIABLE_COMPARISON_OPERATOR
        VIABLE_COMPARISON_OPERATOR -> "at most" | "exactly"
        COMPARISON_RHS -> "t" | "i" | "j"

        FIRST_OR_LAST_TERM_RESTRICTION -> "under the constraint that" RESTRICTED_TERM_INDEX "is part of a" TERM_LENGTH "term"
        RESTRICTED_TERM_INDEX -> "A[1]" | "A[n]" | "A[i]"
        TERM_LENGTH -> "1-digit" | "2-digit" | "3-digit" | "i-digit" | "j-digit"

        EPSILON ->
    """
    )


def get_hotel_cost_coupons_cfg() -> ScaffoldedWritingCFG:
    function_names = concat_into_production_rule(
        ["DP", "Memo", "MinCost", "MaxCost", "MinHotels", "MaxHotels"], ["(i)", "(i,j)"]
    )

    return ScaffoldedWritingCFG.fromstring(
        f"""
        START -> "Let" FUNCTION_DECLARATION "denote the" FUNCTION_OUTPUT "."

        FUNCTION_DECLARATION -> "the subproblem" | {function_names}

        FUNCTION_OUTPUT -> EXTREMAL_ADJ OUTPUT_NOUN "of Momo's trip" SITUATION

        EXTREMAL_ADJ -> EPSILON | "minimum" | "maximum"
        OUTPUT_NOUN -> "answer" | "number of hotels" | "cost"
        SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING | SUBARRAY_RESTRICTION ADDITIONAL_RESTRICTION

        MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j"

        SUBARRAY_RESTRICTION -> EPSILON | "from" SUBARRAY
        SUBARRAY -> "the rest of the trip" | "mile 1 to n" | PREFIX_SUBPROBLEM | SUFFIX_SUBPROBLEM | DOUBLE_ENDED_SUBPROBLEM
        PREFIX_SUBPROBLEM -> "mile 1 to i"
        SUFFIX_SUBPROBLEM -> "mile i to n"
        DOUBLE_ENDED_SUBPROBLEM -> "mile i to j"


        ADDITIONAL_RESTRICTION -> EPSILON | NUM_COUPONS_RESTRICTION | HOTEL_STATUS_RESTRICTION \
                                | NUM_COUPONS_RESTRICTION "and" HOTEL_STATUS_RESTRICTION \
                                | HOTEL_STATUS_RESTRICTION "and" NUM_COUPONS_RESTRICTION

        NUM_COUPONS_RESTRICTION -> "using" COMPARISON_OPERATOR COMPARISON_RHS "coupons"
        COMPARISON_OPERATOR -> "at least" | VIABLE_COMPARISON_OPERATOR
        VIABLE_COMPARISON_OPERATOR -> "at most" | "exactly"
        COMPARISON_RHS -> "k" | "i" | "j"

        HOTEL_STATUS_RESTRICTION -> HOTEL_STATUS "the cost of" RESTRICTED_HOTEL_INDEX
        RESTRICTED_HOTEL_INDEX -> "hotel i" | "hotel j"
        HOTEL_STATUS -> VIABLE_HOTEL_STATUS | "excluding"
        VIABLE_HOTEL_STATUS -> "including"

        EPSILON ->
    """
    )

def get_hotel_cost_cfg() -> ScaffoldedWritingCFG:
    function_names = concat_into_production_rule(
        ["DP", "Memo", "MinCost", "MaxCost", "MinHotels", "MaxHotels"], ["(i)", "(i,j)"]
    )

    return ScaffoldedWritingCFG.fromstring(
        f"""
        START -> "Let" FUNCTION_DECLARATION "denote the" FUNCTION_OUTPUT "."

        FUNCTION_DECLARATION -> "the subproblem" | {function_names}

        FUNCTION_OUTPUT -> EXTREMAL_ADJ OUTPUT_NOUN "of Momo's trip" SITUATION

        EXTREMAL_ADJ -> EPSILON | "minimum" | "maximum"
        OUTPUT_NOUN -> "answer" | "number of hotels" | "cost"
        SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING | SUBARRAY_RESTRICTION ADDITIONAL_RESTRICTION

        MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j"

        SUBARRAY_RESTRICTION -> EPSILON | "from" SUBARRAY
        SUBARRAY -> "the rest of the trip" | "mile 1 to n" | PREFIX_SUBPROBLEM | SUFFIX_SUBPROBLEM | DOUBLE_ENDED_SUBPROBLEM
        PREFIX_SUBPROBLEM -> "mile 1 to i"
        SUFFIX_SUBPROBLEM -> "mile i to n"
        DOUBLE_ENDED_SUBPROBLEM -> "mile i to j"


        ADDITIONAL_RESTRICTION -> EPSILON | HOTEL_STATUS_RESTRICTION

        HOTEL_STATUS_RESTRICTION -> HOTEL_STATUS "the cost of" RESTRICTED_HOTEL_INDEX
        RESTRICTED_HOTEL_INDEX -> "hotel i" | "hotel j"
        HOTEL_STATUS -> VIABLE_HOTEL_STATUS | "excluding"
        VIABLE_HOTEL_STATUS -> "including"

        EPSILON ->
    """
    )


def get_grasslearn_cfg() -> ScaffoldedWritingCFG:
    function_names = concat_into_production_rule(
        ["Memo", "MaxPoints", "MinMinutes", "Streak", "Questions"],
        ["(i)", "(i,j)", "(i,j,k)"],
    )

    return ScaffoldedWritingCFG.fromstring(
        f"""
        START -> "define" FUNCTION_DECLARATION "to be the" FUNCTION_OUTPUT "."

        FUNCTION_DECLARATION -> "the subproblem" | {function_names}

        FUNCTION_OUTPUT -> EXTREMAL_ADJ OUTPUT_NOUN "needed" SITUATION

        EXTREMAL_ADJ -> EPSILON | "minimum" | "maximum"
        OUTPUT_NOUN -> "answer" | "number of questions" | "number of points" | "number of minutes" | "streak"

        SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING \
                | NUM_POINTS_OR_QUESTIONS_RESTRICTION SUBARRAY_RESTRICTION STREAK_RESTRICTION

        MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j" | "for i, j, and k"

        NUM_POINTS_OR_QUESTIONS_RESTRICTION -> EPSILON | NUM_POINTS_RESTRICTION | NUM_QUESTIONS_RESTRICTION
        NUM_POINTS_RESTRICTION -> "to earn" COMPARISON_OPERATOR NUM_POINTS "points"
        NUM_QUESTIONS_RESTRICTION -> "to correctly answer" COMPARISON_OPERATOR NUM_POINTS "questions"

        COMPARISON_OPERATOR -> "at most" | VIABLE_COMPARISON_OPERATOR
        VIABLE_COMPARISON_OPERATOR -> "at least" | "exactly"
        NUM_POINTS -> "p" | "i" | "j" | "k"

        SUBARRAY_RESTRICTION -> EPSILON | "from" SUBARRAY
        SUBARRAY -> "the rest of the questions" | "Questions 1 through n" \
                | PREFIX_SUBPROBLEM | SUFFIX_SUBPROBLEM | DOUBLE_ENDED_SUBPROBLEM
        PREFIX_SUBPROBLEM -> "Questions 1 through i"
        SUFFIX_SUBPROBLEM -> "Questions i through n"
        DOUBLE_ENDED_SUBPROBLEM -> "Questions i through j"

        STREAK_RESTRICTION -> EPSILON | STARTING_OR_ENDING "with a streak of length" STREAK_LENGTH
        STARTING_OR_ENDING -> "starting" | "ending"
        STREAK_LENGTH -> "i" | "j" | "k"

        EPSILON ->
    """
    )


def get_grasslearn_2var_cfg() -> ScaffoldedWritingCFG:
    function_names = concat_into_production_rule(
        ["Memo", "MaxPoints", "MinMinutes", "Questions"],
        ["(i)", "(i,j)", "(i,j,k)"],
    )

    return ScaffoldedWritingCFG.fromstring(
        f"""
        START -> "define" FUNCTION_DECLARATION "to be the" FUNCTION_OUTPUT "."

        FUNCTION_DECLARATION -> "the subproblem" | {function_names}

        FUNCTION_OUTPUT -> EXTREMAL_ADJ OUTPUT_NOUN "needed" SITUATION

        EXTREMAL_ADJ -> EPSILON | "minimum" | "maximum"
        OUTPUT_NOUN -> "answer" | "number of questions" | "number of points" | "number of minutes"

        SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING \
                | NUM_POINTS_OR_QUESTIONS_RESTRICTION SUBARRAY_RESTRICTION

        MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j" | "for i, j, and k"

        NUM_POINTS_OR_QUESTIONS_RESTRICTION -> EPSILON | NUM_POINTS_RESTRICTION | NUM_QUESTIONS_RESTRICTION
        NUM_POINTS_RESTRICTION -> "to earn" COMPARISON_OPERATOR NUM_POINTS "points"
        NUM_QUESTIONS_RESTRICTION -> "to correctly answer" COMPARISON_OPERATOR NUM_POINTS "questions"

        COMPARISON_OPERATOR -> "at most" | VIABLE_COMPARISON_OPERATOR
        VIABLE_COMPARISON_OPERATOR -> "at least" | "exactly"
        NUM_POINTS -> "p" | "i" | "j" | "k"

        SUBARRAY_RESTRICTION -> EPSILON | "from" SUBARRAY
        SUBARRAY -> "the rest of the questions" | "Questions 1 through n" \
                | PREFIX_SUBPROBLEM | SUFFIX_SUBPROBLEM | DOUBLE_ENDED_SUBPROBLEM
        PREFIX_SUBPROBLEM -> "Questions 1 through i"
        SUFFIX_SUBPROBLEM -> "Questions i through n"
        DOUBLE_ENDED_SUBPROBLEM -> "Questions i through j"

        EPSILON ->
    """
    )



def get_max_profit_cfg() -> ScaffoldedWritingCFG:
    function_names = concat_into_production_rule(
        ["DP", "Memo", "MaxProfit"], ["(i)", "(i,j)"]
    )

    return ScaffoldedWritingCFG.fromstring(
        f"""
        START -> "define" FUNCTION_DECLARATION "to be the" FUNCTION_OUTPUT "."

        FUNCTION_DECLARATION -> "the subproblem" | {function_names}

        FUNCTION_OUTPUT -> EXTREMAL_ADJ OUTPUT_NOUN "that can be obtained" SITUATION

        EXTREMAL_ADJ -> EPSILON | "minimum" | "maximum"
        OUTPUT_NOUN -> "answer" | "profit"
        SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING | SUBARRAY_RESTRICTION \
                | NUM_TRIALS_RESTRICTION SUBARRAY_RESTRICTION

        MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j"

        SUBARRAY_RESTRICTION -> EPSILON | "from" SUBARRAY
        SUBARRAY -> "the rest of the trials" | "Trials 1 through n" \
                | PREFIX_SUBPROBLEM | SUFFIX_SUBPROBLEM | DOUBLE_ENDED_SUBPROBLEM
        PREFIX_SUBPROBLEM -> "Trials 1 through i"
        SUFFIX_SUBPROBLEM -> "Trials i through n"
        DOUBLE_ENDED_SUBPROBLEM -> "Trials i through j"

        NUM_TRIALS_RESTRICTION -> "by accepting" COMPARISON_OPERATOR COMPARISON_RHS "trials"
        COMPARISON_OPERATOR -> "at least" | "at most" | "exactly"
        COMPARISON_RHS -> "i" | "j"

        EPSILON ->
    """
    )


def get_valid_shuffle_cfg() -> ScaffoldedWritingCFG:
    function_names = concat_into_production_rule(
        ["DP", "Memo", "ValidShuffle"],
        [
            "(i)",
            "(i,j)",
            "(i,j,k)",
        ],
    )

    return ScaffoldedWritingCFG.fromstring(
        f"""
        START -> "define" FUNCTION_DECLARATION "to be" FUNCTION_OUTPUT "."

        FUNCTION_DECLARATION -> "the subproblem" | {function_names}
        FUNCTION_OUTPUT -> BOOL SITUATION FALSE_CASE
        BOOL -> "True" | "False"

        SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING | SUBARRAY_RESTRICTION
        MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j" | "for i, j, and k"
        SUBARRAY_RESTRICTION -> EPSILON | "if" SUBARRAY
        SUBARRAY -> DEFC "is a valid shuffle of" DEFA "and" DEFB

        DEFC -> "C" | "C[i]" | "C[j]" | "C[k]" | "C[1..i]" | "C[1..j]" | "C[1..k]" | "C[1..i+j]"
        DEFA -> "A" | "A[i]" | "A[j]" | "A[1..i]" | "A[1..j]"
        DEFB -> "B" | "B[i]" | "B[j]" | "B[1..i]" | "B[1..j]"

        FALSE_CASE -> EPSILON | "and" BOOL "otherwise"

        EPSILON ->
        """
    )


def get_lcs_cfg() -> ScaffoldedWritingCFG:
    function_names = concat_into_production_rule(
        ["DP", "Memo", "LCS"],
        [
            "(i)",
            "(i,j)",
            "(i,j,k)",
        ],
    )

    return ScaffoldedWritingCFG.fromstring(
        f"""
        START -> "define" FUNCTION_DECLARATION "to be the" FUNCTION_OUTPUT "."

        FUNCTION_DECLARATION -> "the subproblem" | {function_names}
        FUNCTION_OUTPUT -> OUTPUT_NOUN SITUATION
        OUTPUT_NOUN -> "answer" | "number of longest common subsequences" \
                | "length of the longest common subsequence"

        SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING | SUBARRAY_RESTRICTION
        MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j" | "for i, j, and k"
        SUBARRAY_RESTRICTION -> EPSILON | "between" SUBARRAY
        SUBARRAY -> DEFA "and" DEFB

        DEFA -> "A[1..n]" | VALID_DEFA | DOUBLE_ENDED_A
        DEFB -> "B[1..m]" | VALID_DEFB | DOUBLE_ENDED_B

        VALID_DEFA -> "A[1..i]" | "A[1..j]" | "A[i..n]" | "A[j..n]"
        VALID_DEFB -> "B[1..i]" | "B[1..j]" | "B[i..m]" | "B[j..m]"
        DOUBLE_ENDED_A -> "A[i..j]" | "A[i..k]" | "A[j..k]"
        DOUBLE_ENDED_B -> "B[i..j]" | "V[i..k]" | "B[j..k]"

        EPSILON ->
        """
    )
