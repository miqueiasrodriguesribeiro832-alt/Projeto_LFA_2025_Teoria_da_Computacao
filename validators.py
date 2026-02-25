def is_deterministic(automaton, verbose=False):
    seen = set()

    for (state, symbol) in automaton.transitions:
        if (state, symbol) in seen:
            if verbose:
                 print(f"❌ Não determinístico: mais de uma transição para ({state},{symbol})")
            return False
        seen.add((state, symbol))

    if verbose:
         print("✔ Verificação de determinismo: AFD é determinístico")
    return True

# Verificar se a função de transição é total
def make_complete(automaton, verbose=False):
    sink = "A"
    created = False

    for state in list(automaton.states):
        for symbol in automaton.alphabet:
            if (state, symbol) not in automaton.transitions:
                if not created:
                    automaton.states.add(sink)
                    created = True
                    if verbose:
                        print("⚠ Função de transição não é total → criando estado artificial A")

                automaton.transitions[(state, symbol)] = sink
                if verbose:
                    print(f"  δ({state},{symbol}) = A")

    if created:
        for symbol in automaton.alphabet:
            automaton.transitions[(sink, symbol)] = sink

        if verbose:
            print("✔ Função de transição agora é total")
    else:
        if verbose:
            print("✔ Função de transição já era total")

# Estados alcançáveis
def reachable_states(automaton):
    visited = set()
    stack = [automaton.initial_state]

    while stack:
        state = stack.pop()
        if state not in visited:
            visited.add(state)

            for symbol in automaton.alphabet:
                next_state = automaton.transitions.get((state, symbol))
                if next_state and next_state not in visited:
                    stack.append(next_state)

    return visited

# Agora removemos os estados inválidos
def remove_unreachable(automaton, verbose=False):
    reachable = reachable_states(automaton)
    unreachable = automaton.states - reachable

    if verbose:
        if unreachable:
            print(f"⚠ Estados inalcançáveis removidos: {unreachable}")
        else:
            print("✔ Todos os estados são alcançáveis")

    automaton.states = reachable
    automaton.final_states &= reachable

    automaton.transitions = {
        (s, a): t
        for (s, a), t in automaton.transitions.items()
        if s in reachable
    }
