# SIMULAÇÃO DE AFN
def simulate_afn(afn, word, verbose=True):
    current_states = {afn.initial_state}

    if verbose:
        print("Estados iniciais:", current_states)

    for symbol in word:
        next_states = set()
        for state in current_states:
            next_states |= afn.transitions.get((state, symbol), set())

        current_states = next_states

        if verbose:
            print(f"Lendo '{symbol}' → {current_states}")

        if not current_states:
            break

    if any(s in afn.final_states for s in current_states):
        print("PALAVRA ACEITA")
        return True
    else:
        print("PALAVRA REJEITADA")
        return False
