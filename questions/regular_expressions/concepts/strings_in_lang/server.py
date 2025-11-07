import random

from theorielearn.automata_utils.fa_utils import sample_input_strings
from theorielearn.regular_expressions.parser import compute_nfa_from_regex_lines
from theorielearn.regular_expressions.utils import convert_regex_to_latex
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    variants = [
        "(e+1)(01)*(e+0)",
        "(0+1)*010(0+1)*",
        "1*(01*01*)*",
        "0+1(0+1)*00",
        "((e+0+00+000)1)*(e+0+00+000)",
        "(0+1)(0+1)(0+1)(0+1)*",
        "((0+1)(0+1))*",
        "(1*0)*(0*1)*",
        "(00000)*",
        "0(0+1(1+0(0+11*)*)*)*",
    ]

    max_length_to_check = 8
    num_rand_choices = 10
    choice = random.choice(variants)

    nfa = compute_nfa_from_regex_lines(choice)

    (sampled_accepted, sampled_not_accepted) = sample_input_strings(
        max_length_to_check, num_rand_choices, nfa
    )

    data["params"]["strings_in_lang"] = sampled_accepted
    data["params"]["strings_not_in_lang"] = sampled_not_accepted

    data["params"]["regex"] = convert_regex_to_latex(choice)
