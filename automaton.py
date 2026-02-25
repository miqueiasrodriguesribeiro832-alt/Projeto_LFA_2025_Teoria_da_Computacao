class Automaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions # dict: (state, symbol) -> state
        self.initial_state = initial_state
        self.final_states = set(final_states)

    def show(self):
        print("\n=== AFD GERADO ===\n")

        print("Estados:", self.states)
        print("Alfabeto:", self.alphabet)
        print("Estado inicial:", self.initial_state)
        print("Estados finais:", self.final_states)

        print("\nFunção de Transição:")
        for (s, a), t in self.transitions.items():
            print(f"δ({s},{a}) = {t}")

        print("\n====================\n")

    def show_graph_format(self):
        print("\n=== DIAGRAMA (Formato Texto) ===\n")

        for (s, a), t in self.transitions.items():
            print(f"{s} --{a}--> {t}")

        print("\n===============================\n")

