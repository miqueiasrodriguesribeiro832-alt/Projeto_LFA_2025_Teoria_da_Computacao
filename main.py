#           Trabalho de Teoria da Computação
#           Aluno: [ Miquéias Rodrigues Ribeiro
#                    Linda Inez Rodrigues Ribeiro
#                    Jesus Clarindo Pinheiro ]      
#           UFPA 2025.2



from automaton import Automaton
from dfa_simulator import DFASimulator
from validators import is_deterministic, make_complete, remove_unreachable
from minimizer import build_pairs, mark_trivial, mark_by_transitions, find_equivalences, build_groups, build_minimized_automaton
from nfa import AFN
from nfa_simulator import simulate_afn
from nfa_to_dfa import afn_to_afd
from grammar import *



#
def create_automaton():
    states = input("Estados (ex: q0,q1,q2): ").split(",")
    alphabet = input("Alfabeto (ex: 0,1): ").split(",")

    transitions = {}
    print("Defina as transições δ(q,a)=p")

    for s in states:
        for a in alphabet:
            t = input(f"Transição: δ({s}, {a}) = ")
            transitions[(s,a)] = t

    initial = input("Estado inicial: ")
    finals = input("Estados finais (ex: q1,q2): ").split(",")

    return Automaton(states, alphabet, transitions, initial, finals)

#CRIAÇÃO DE AFN
def create_afn():
    states = set(s.strip() for s in input("Estados: ").split(","))
    alphabet = set(a.strip() for a in input("Alfabeto: ").split(","))

    transitions = {}
    print("\nDefina as transições do AFN.")
    print("Digite os estados de destino separados por vírgula.")
    print("Deixe em branco se não houver transição.\n")

    for s in states:
        for a in alphabet:
            dest = input(f"Transição: δ({s},{a}) = ").strip()
            if dest:
                targets = set(t.strip() for t in dest.split(","))
                transitions[(s, a)] = targets

    initial = input("\nEstado inicial: ").strip()
    finals = set(f.strip() for f in input("Estados finais: ").split(","))

    return AFN(states, alphabet, transitions, initial, finals)

# CRIAR FUNÇÃO PARA DEFINIR GRAMÁTICA
def create_grammar():
    print("\n=== DEFINIR GRAMÁTICA ===\n")

    N = set(nt.strip() for nt in input("Não-terminais (ex: S,A,B): ").split(","))
    T = set(t.strip() for t in input("Terminais (ex: a,b): ").split(","))

    productions = {}

    print("\nDigite as produções no formato:")
    print("Exemplo: S -> aA | b")
    print("Pressione ENTER para finalizar.\n")

    while True:
        line = input("Produção: ").strip()
        if not line:
            break

        left, right = line.split("->")
        left = left.strip()
        right = right.strip()

        rules = [r.strip() for r in right.split("|")]

        productions.setdefault(left, []).extend(rules)

    S = input("\nSímbolo inicial: ").strip()

    print("\nGramática criada com sucesso!")
    return Grammar(N, T, productions, S)

automaton = None
minimized = None
afn = None
while True:
    print("\n--- MENU ---")
    print("1 - Criar AFD")
    print("2 - Testar palavra")
    print("3 - Minimizar AFD")
    print("4 - Testar palavras no AFD mínimo")
    print("5 - Criar AFN")
    print("6 - Testar paravra no AFN")
    print("7 - Converter AFN -> AFD")
    print("8 - Definir Gramática")
    print("9 - Classificar Gramática")
    print("10 - Converter GR → AFD")
    print("11 - Gerar Derivação")
    print("12 - Gerar Árvore de Derivação")
    print("13 - Analisar estrutura da gramática GLC")
    print("14 - Simplificação completa automática da GLC")
    print("15 - Gerar pseudocódigo do reconhecedor")
    print("0 - Sair\n")

    op = input("Escolha: ")

    if op == "1":
        automaton = create_automaton()
        print("AFD criado com sucesso!")

    elif op == "2":
        if not automaton:
            print("Crie um AFD primeiro.")
            continue

        w = input("Palavra: ")
        sim = DFASimulator(automaton)
        ok, log = sim.simulate(w)

        for l in log:
            print(l)

    elif op == "3":
        print("\n=== INÍCIO DA MINIMIZAÇÃO ===\n")
        if not automaton:
            print("Crie um AFD primeiro.")
            continue

        print("\nVerificando AFD...")

        if not is_deterministic(automaton, verbose=True):
            print("Não é determinísco. Não pode minimizar.")
            continue

        make_complete(automaton, verbose=True)
        remove_unreachable(automaton, verbose=True)

        pairs = build_pairs(automaton.states, verbose=True)
        marked = mark_trivial(pairs, automaton.final_states, verbose=True)
        mark_by_transitions(pairs, marked, automaton, verbose=True)

        unmarked_pairs = [p for p in pairs if p not in marked]
        eq = find_equivalences(unmarked_pairs, marked)
        groups = build_groups(automaton.states, eq, verbose=True)

        ns, nt, ni,nf = build_minimized_automaton(automaton, groups)

        minimized = Automaton(ns, automaton.alphabet, nt, ni, nf)

        print("AFD minimizado com sucesso!")
        print("Grupos de estados:", groups)
        print("\n=== FIM DA MINIMIZAÇÃO ===")

    elif op == "4":
        if not minimized:
            print("Minimize primeiro.")
            continue

        w = input("Palavra: ")
        sim = DFASimulator(minimized)
        ok, log = sim.simulate(w)

        for l in log:
            print(l)

    elif op == "5":
        afn = create_afn()
        print("AFN criado com sucesso!")


    elif op == "6":
        if not afn:
            print("Crie uma AFN primeiro.")
            continue
        
        word = input("Digite a palavra: ")
        simulate_afn(afn, word)

    elif op == "7":
        if not afn:
            print("Crie a AFN primeiro.")
            continue
        automaton = afn_to_afd(afn, verbose=True)
        print("AFD gerado a partir do AFN com sucesso!")

    elif op == "8":
        grammar = create_grammar()

    elif op == "9":
        if grammar:
            tipo = grammar.classify()
            print(f"\nTipo da Gramática: {tipo}")
        else:
            print("Defina uma gramática primeiro.")

    elif op == "10":
        if grammar:
            if grammar.classify() == "GR":
                states, alphabet, transitions, initial, finals = grammar.to_afd()
                automaton = Automaton(states, alphabet, transitions, initial, finals)
                print("\nAFD gerado a partir da Gramática Regular!")
                automaton.show()
                automaton.show_graph_format()

            else:
                print("A gramática não é regular.")
        else:
            print("Defina uma gramática primeiro.")
        
    elif op == "11":
        if grammar:
            w = input("Palavra: ")
            grammar.derive(w)
        else:
            print("Defina uma gramática primeiro.")

    elif op == "12":
        if grammar:
            w = input("Palavra: ")
            grammar.generate_tree(w)
        else:
            print("Defina uma gramática primeiro.")

    elif op == "13":
        if grammar:
            grammar.analyze_structure()
        else:
            print("Defina uma gramática primeiro.")

    elif op == "14":
        if grammar:
            grammar.simplify_complete()
        else:
            print("Defina uma gramática primeiro.")

    elif op == "15":
        if grammar:
            grammar.generate_recognizer_pseudocode()
        else:
            print("Defina uma gramática primeiro.")

    elif op == "0":
        break



