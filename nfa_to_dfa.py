# CONVERSÃO AFN → AFD
from automaton import Automaton

def afn_to_afd(afn, verbose=True):
    initial = frozenset([afn.initial_state])
    states = {initial}
    transitions = {}
    finals = set()
    queue = [initial]

    while queue:
        current = queue.pop(0)

        if verbose:
            print("Processando estado:", set(current))

        for symbol in afn.alphabet:
            next_state = set()
            for s in current:
                next_state |= afn.transitions.get((s, symbol), set())

            next_state = frozenset(next_state)
            transitions[(current, symbol)] = next_state

            if next_state not in states:
                states.add(next_state)
                queue.append(next_state)

    for state in states:
        if any(s in afn.final_states for s in state):
            finals.add(state)

    return Automaton(states, afn.alphabet, transitions, initial, finals)
