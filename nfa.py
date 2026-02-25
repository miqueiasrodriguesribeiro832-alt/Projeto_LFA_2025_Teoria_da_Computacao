class AFN:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  # (estado, símbolo) -> set(estados)
        self.initial_state = initial_state
        self.final_states = final_states
