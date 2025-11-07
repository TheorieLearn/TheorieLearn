from typing import Any, Dict, List, Tuple, Union

import chevron
import prairielearn as pl
from automata.fa.dfa import DFA
from automata.fa.fa import FAStateT
from automata.fa.nfa import NFA
from theorielearn.automata_utils.fa_utils import states_to_string
from theorielearn.shared_utils import grade_question_tokenized


def generate(
    data: Dict[str, Any],
    transformation_name: str,
    transformation_definition: str,
    description_of_states: str,
    M: DFA,
    M_prime: Union[DFA, NFA],
    transitions_to_ask: List[Tuple[FAStateT, str]],
) -> None:
    data["correct_answers"]["Q'"] = states_to_string(M_prime.states)
    data["correct_answers"]["s'"] = states_to_string(M_prime.initial_state)
    data["correct_answers"]["A'"] = states_to_string(M_prime.final_states)

    transition_question_names = []
    for q, a in transitions_to_ask:
        question_name = rf"\delta'({states_to_string(q)}, {states_to_string(a)})"
        transition_question_names.append(question_name)
        data["correct_answers"][question_name] = states_to_string(
            M_prime.transitions[q][a]
        )

    with open(
        data["options"]["server_files_course_path"]
        + "/theorielearn/regular_transformation_concrete_example/question_base.html"
    ) as f:
        data["params"]["html"] = chevron.render(
            f,
            {
                "transformation_name": transformation_name,
                "transformation_definition": transformation_definition,
                "description_of_states": description_of_states,
                "dfa_diagram": M.show_diagram().string(),
                "transitions_to_ask": transition_question_names,
                "M'_is_nfa": type(M_prime) is NFA,
            },
        ).strip()


def grade(data: pl.QuestionData) -> None:
    for question_name in data["correct_answers"].keys():
        grade_question_tokenized(data, question_name)
    pl.set_weighted_score_data(data)
