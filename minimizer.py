# Construir todos os pares de estados
def build_pairs(states, verbose=False):
    pairs = set()
    states = list(states)

    for i in range(len(states)):
        for j in range(i+1, len(states)):
            pairs.add((states[i], states[j]))

    if verbose:
        print("✔ Tabela de pares construída:")
        for p in pairs:
            print(" ", p)

    return pairs

# Marcar os trivialmente não equivalentes
def mark_trivial(pairs, final_states, verbose=False):
    marked = set()

    for (p, q) in pairs:
        if (p in final_states) != (q in final_states):
            marked.add((p, q))
            if verbose:
                print(f"❌ Marcando par trivialmente não equivalente: ({p},{q})")

    if verbose:
        print("✔ Marcação trivial concluída")

    return marked

# Marcação por dependência
def mark_by_transitions(pairs, marked, automaton, verbose=False):
    changed = True

    while changed:
        changed = False

        for (p, q) in pairs:
            if (p, q) in marked:
                continue

            for symbol in automaton.alphabet:
                p1 = automaton.transitions[(p, symbol)]
                q1 = automaton.transitions[(q, symbol)]

                pair = tuple(sorted((p1, q1)))

                if pair in marked:
                    marked.add((p, q))
                    changed = True
                    if verbose:
                        print(f"❌ Marcando ({p},{q}) pois δ({p},{symbol})={p1} e δ({q},{symbol})={q1}")
                    break

    if verbose:
        print("✔ Marcação por análise concluída")

# Encontrar equivalentes
def find_equivalences(pairs, marked):
    eq = []

    for pair in pairs:
        if pair not in marked:
            eq.append(pair)

    return eq

# Unificar estados
def build_groups(states, equivalences, verbose=False):
    groups = []

    for s in states:
        found = False
        for g in groups:
            if any((s, x) in equivalences or (x, s) in equivalences for x in g):
                g.add(s)
                found = True
                break
        if not found:
            groups.append({s})

    if verbose:
        print("✔ Estados equivalentes (grupos finais):")
        for g in groups:
            print(" ", g)

    return groups

def state_to_str(s):
    if isinstance(s, frozenset):
        return "_".join(sorted(s))
    return str(s)

# Construir o novo AFD mínimo
def build_minimized_automaton(automaton, groups):
    new_states = set()
    new_transitions = {}
    new_finals = set()

    repr_map = {}

    for g in groups:
        nome = "_".join(sorted(g) for s in g)
        new_states.add(nome)

        for s in g:
            repr_map[s] = nome

        if g & automaton.final_states:
            new_finals.add(nome)

    new_initial = repr_map[automaton.initial_state]

    for (s, a), t in automaton.transitions.items():
        new_transitions[(repr_map[s], a)] = repr_map[t]

    return new_states, new_transitions, new_initial, new_finals