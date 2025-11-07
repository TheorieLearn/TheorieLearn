from automata.fa.dfa import DFA

states = {"e", "0", "01", "010", "0100"}
input_symbols = {"0", "1"}

transitions = {
    "e": {"0": "0", "1": "e"},
    "0": {"0": "0", "1": "01"},
    "01": {"0": "010", "1": "e"},
    "010": {"0": "0100", "1": "e"},
    "0100": {"0": "0100", "1": "0100"},
}

initial_state = "e"
final_states = {"0100"}

fa = DFA(
    states=states,
    input_symbols=input_symbols,
    transitions=transitions,
    initial_state=initial_state,
    final_states=final_states,
)
