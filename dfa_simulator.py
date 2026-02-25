class DFASimulator:
    def __init__(self, automaton):
        self.automaton = automaton

    def simulate(self, word):
        current_state = self.automaton.initial_state
        log = []

        log.append(f"Estado inicial: {current_state}")

        for symbol in word:
            log.append(f"Lendo símbolo: {symbol}")

            key = (current_state, symbol)

            if key not in self.automaton.transitions:
                log.append(f"Não existe δ({current_state}, {symbol} -> rejeita)")
                return False, log
            
            next_state = self.automaton.transitions[key]

            log.append(f"δ({current_state}, {symbol}) = {next_state}")

            current_state = next_state

        log.append(f"Fim da palavra. Estado final: {current_state}")

        if current_state in self.automaton.final_states:
            log.append("O estado é final -> PALAVRA ACEITA")
            return True, log
        else:
            log.append("O estado não é final -> PALAVRA REJEITADA")
            return False, log