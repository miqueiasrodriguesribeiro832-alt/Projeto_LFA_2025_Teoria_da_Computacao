
class Node:
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []


class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def classify(self):
        for left, rules in self.productions.items():

            # Verifica se lado esquerdo é apenas 1 não-terminal
            if left not in self.non_terminals:
                return "GLC"

            for rule in rules:

                # Permite epsilon
                if rule == "ε":
                    continue

                # Caso 1: apenas 1 símbolo
                if len(rule) == 1:
                    if rule not in self.terminals:
                        return "GLC"

                # Caso 2: 2 símbolos
                elif len(rule) == 2:
                    if rule[0] not in self.terminals:
                        return "GLC"
                    if rule[1] not in self.non_terminals:
                        return "GLC"

                else:
                    return "GLC"

        return "GR"

    def to_afd(self, verbose=True):
        states = set(self.non_terminals)
        alphabet = set(self.terminals)
        transitions = {}
        final_states = set()

        final_state = "F"
        states.add(final_state)

        if verbose:
            print("\n=== CONVERSÃO GR → AFD ===\n")

        for left, rules in self.productions.items():

            for rule in rules:

                if verbose:
                    print(f"Analisando produção: {left} → {rule}")

                # Caso epsilon
                if rule == "ε":
                    final_states.add(left)
                    if verbose:
                        print(f"  → {left} é estado final (ε-produção)")

                # Caso A → a
                elif len(rule) == 1:
                    # Se já existe transição com esse símbolo,
                    # apenas marque o destino como final
                    if (left, rule) in transitions:
                        destino = transitions[(left, rule)]
                        final_states.add(destino)
                    else:
                        transitions[(left, rule)] = final_state
                    if verbose:
                        print(f"  → Criando transição: δ({left},{rule}) = {final_state}")

                # Caso A → aB
                elif len(rule) == 2:
                    a = rule[0]
                    B = rule[1]
                    transitions[(left, a)] = B
                    if verbose:
                        print(f"  → Criando transição: δ({left},{a}) = {B}")

        final_states.add(final_state)

        if verbose:
            print("\nEstado final artificial criado:", final_state)
            print("\n=== FIM DA CONVERSÃO ===\n")

        initial_state = self.start_symbol

        return states, alphabet, transitions, initial_state, final_states

    def derive(self, word):
        print("\n=== DERIVAÇÃO ===\n")

        path = []
        success = self._derive_recursive(self.start_symbol, word, path)

        if success:
            print("Sequência de derivações:")
            for step in path:
                print(step)
            print("\nPALAVRA DERIVADA COM SUCESSO!")
            return path
        else:
            print("\nNão foi possível derivar a palavra.")
            return None

    def _derive_recursive(self, current, word, path):

        # Se só tem terminais
        if all(symbol not in self.non_terminals for symbol in current):
            if current == word:
                return True
            return False

        # Poda inteligente
        terminals_only = "".join(
            s for s in current if s in self.terminals
        )

        if not word.startswith(terminals_only):
            return False

        for i, symbol in enumerate(current):

            if symbol in self.non_terminals:

                for production in self.productions.get(symbol, []):

                    new_string = current[:i] + production + current[i+1:]

                    temp_path = []

                    if self._derive_recursive(new_string, word, temp_path):

                        # salva o passo corretamente
                        path.append(f"{current} ⇒ {new_string}")
                        path.extend(temp_path)
                        return True

                return False

        return False

    def generate_tree(self, word):
        print("\n=== ÁRVORE DE DERIVAÇÃO ===\n")

        path = []
        success = self._derive_recursive(self.start_symbol, word, path)

        if not success:
            print("Não foi possível gerar árvore para essa palavra.")
            return

        root = Node(self.start_symbol)

        self._build_tree_from_path(root, path)

        self._print_slash_tree(root)

        print("\nPALAVRA DERIVADA COM SUCESSO!")

    def _build_tree_from_path(self, root, path):

        nodes = [root]

        for step in path:
            if "⇒" not in step:
                continue

            left, right = step.split(" ⇒ ")

            # encontra o primeiro não-terminal ainda não expandido
            for node in nodes:
                if node.symbol in self.non_terminals and not node.children:
                    target = node
                    break
            else:
                continue

            # descobrir qual produção foi usada comparando tamanhos
            for production in self.productions[target.symbol]:

                # gera possível expansão
                if production in right:
                    for symbol in production:
                        new_node = Node(symbol)
                        target.children.append(new_node)

                        if symbol in self.non_terminals:
                            nodes.append(new_node)
                    break

    def _build_tree_bt(self, current, word):

        # Se não tem não-terminais
        if all(symbol not in self.non_terminals for symbol in current):
            if current == word:
                node = Node(current)
                return True, node
            return False, None

        if len(current) > len(word):
            return False, None

        for i, symbol in enumerate(current):

            if symbol in self.non_terminals:

                for production in self.productions.get(symbol, []):

                    new_string = current[:i] + production + current[i+1:]

                    success, subtree = self._build_tree_bt(new_string, word)

                    if success:
                        parent = Node(symbol)

                        for s in production:
                            parent.children.append(Node(s))

                        return True, parent

                return False, None

        return False, None

    def _print_slash_tree(self, node, indent=8):

        # Imprime o nó atual
        print(" " * indent + node.symbol)

        if len(node.children) == 2:
            print(" " * (indent - 1) + "/ \\")
            print(" " * (indent - 2) +
                node.children[0].symbol + "   " +
                node.children[1].symbol)

            # Expande filho direito recursivamente
            self._print_subtree(node.children[1], indent + 4)

        elif len(node.children) == 1:
            print(" " * indent + "|")
            print(" " * indent + node.children[0].symbol)

            # Continua expandindo recursivamente
            self._print_subtree(node.children[0], indent + 4)

    def _print_subtree(self, node, indent):

        if not node.children:
            return

        print(" " * indent + "|")
        print(" " * indent + node.children[0].symbol)

        self._print_subtree(node.children[0], indent + 4)

    def remove_non_generating(self):
        print("\n=== REMOVENDO SÍMBOLOS NÃO GERADORES ===\n")

        generating = set()

        # Passo 1: produções só com terminais
        for nt in self.non_terminals:
            for prod in self.productions.get(nt, []):
                if all(symbol in self.terminals for symbol in prod):
                    generating.add(nt)

        # Passo 2: propagação
        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                if nt not in generating:
                    for prod in self.productions.get(nt, []):
                        if all(symbol in generating or symbol in self.terminals for symbol in prod):
                            generating.add(nt)
                            changed = True

        print("Símbolos geradores:", generating)

        # Remover não geradores
        self.non_terminals = {nt for nt in self.non_terminals if nt in generating}
        self.productions = {
            nt: [prod for prod in prods
                if all(symbol in generating or symbol in self.terminals for symbol in prod)]
            for nt, prods in self.productions.items()
            if nt in generating
        }

        print("Gramática atualizada.")

    def remove_unreachable(self):
        print("\n=== REMOVENDO SÍMBOLOS INALCANÇÁVEIS ===\n")

        reachable = set()
        reachable.add(self.start_symbol)

        changed = True
        while changed:
            changed = False
            for nt in list(reachable):
                for prod in self.productions.get(nt, []):
                    for symbol in prod:
                        if symbol in self.non_terminals and symbol not in reachable:
                            reachable.add(symbol)
                            changed = True

        print("Símbolos alcançáveis:", reachable)

        # Remover inalcançáveis
        self.non_terminals = {nt for nt in self.non_terminals if nt in reachable}

        self.productions = {
            nt: prods
            for nt, prods in self.productions.items()
            if nt in reachable
        }

        print("Gramática atualizada.")

    def remove_epsilon(self):
        print("\n=== REMOVENDO PRODUÇÕES ε ===\n")

        nullable = set()

        #Encontrar quem produz ε diretamente
        for nt in self.non_terminals:
            if "ε" in self.productions.get(nt, []):
                nullable.add(nt)

        #Propagação
        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                for prod in self.productions.get(nt, []):
                    if all(symbol in nullable for symbol in prod):
                        if nt not in nullable:
                            nullable.add(nt)
                            changed = True

        print("Símbolos anuláveis:", nullable)

        new_productions = {}

        #Criar novas produções
        for nt in self.non_terminals:
            new_prods = set()

            for prod in self.productions.get(nt, []):

                if prod == "ε":
                    continue

                new_prods.add(prod)

                # gerar combinações removendo anuláveis
                for i, symbol in enumerate(prod):
                    if symbol in nullable:
                        new_prod = prod[:i] + prod[i+1:]
                        if new_prod != "":
                            new_prods.add(new_prod)

            new_productions[nt] = list(new_prods)

        self.productions = new_productions

        print("Produções atualizadas.")

    def remove_unitary(self):
        print("\n=== REMOVENDO PRODUÇÕES UNITÁRIAS ===\n")

        unitary_pairs = set()

        #Encontrar produções unitárias diretas
        for nt in self.non_terminals:
            for prod in self.productions.get(nt, []):
                if prod in self.non_terminals:
                    unitary_pairs.add((nt, prod))

        #Fechamento transitivo
        changed = True
        while changed:
            changed = False
            new_pairs = set(unitary_pairs)

            for (A, B) in unitary_pairs:
                for (C, D) in unitary_pairs:
                    if B == C and (A, D) not in unitary_pairs:
                        new_pairs.add((A, D))
                        changed = True

            unitary_pairs = new_pairs

        print("Pares unitários encontrados:", unitary_pairs)

        #Copiar produções
        new_productions = {}

        for nt in self.non_terminals:
            new_productions[nt] = []

            # manter produções não unitárias
            for prod in self.productions.get(nt, []):
                if prod not in self.non_terminals:
                    new_productions[nt].append(prod)

            # adicionar produções herdadas
            for (A, B) in unitary_pairs:
                if A == nt:
                    for prod in self.productions.get(B, []):
                        if prod not in self.non_terminals:
                            if prod not in new_productions[nt]:
                                new_productions[nt].append(prod)

        self.productions = new_productions

        print("Produções unitárias removidas.")

    def check_glud(self):
        print("\n=== VERIFICANDO SE É GLUD ===\n")

        is_glud = True

        for nt in self.non_terminals:
            for prod in self.productions.get(nt, []):

                # Caso A → a
                if len(prod) == 1:
                    if prod not in self.terminals:
                        print(f"❌ Problema: {nt} → {prod} não é terminal.")
                        is_glud = False

                # Caso A → aB
                elif len(prod) == 2:
                    if prod[0] not in self.terminals or prod[1] not in self.non_terminals:
                        print(f"❌ Problema: {nt} → {prod} não está na forma aB.")
                        is_glud = False

                else:
                    print(f"❌ Problema: {nt} → {prod} tem mais de 2 símbolos.")
                    is_glud = False

        if is_glud:
            print("✅ A gramática já está na forma GLUD!")
        else:
            print("\n⚠ A gramática NÃO está na forma GLUD.")

        return is_glud

    def simplify_complete(self):
        print("\n====================================")
        print("     SIMPLIFICAÇÃO COMPLETA")
        print("====================================\n")

        # Mostrar gramática original
        print("📌 Gramática Original:\n")
        for nt in self.productions:
            for prod in self.productions[nt]:
                print(f"{nt} → {prod}")

        print("\n------------------------------------\n")

        # Etapas
        print("1️ Removendo não geradores...")
        self.remove_non_generators()

        print("\n2️ Removendo inalcançáveis...")
        self.remove_unreachable()

        print("\n3️ Removendo produções ε...")
        self.remove_epsilon()

        print("\n4️ Removendo produções unitárias...")
        self.remove_unitary()

        print("\n------------------------------------\n")

        # Mostrar gramática final
        print("📌 Gramática Após Simplificação:\n")
        for nt in self.productions:
            for prod in self.productions[nt]:
                print(f"{nt} → {prod}")

        print("\n5️ Verificando se é GLUD...\n")
        is_glud = self.check_glud()

        print("\n====================================")
        if is_glud:
            print("✅ RESULTADO FINAL: Gramática está na forma GLUD.")
        else:
            print("⚠ RESULTADO FINAL: Gramática NÃO está na forma GLUD.")
        print("====================================\n")

    def analyze_structure(self):
        print("\n====================================")
        print("     ANÁLISE ESTRUTURAL")
        print("====================================\n")

        problems = False

        for nt in self.productions:
            for prod in self.productions[nt]:

                non_terminals_count = sum(1 for s in prod if s in self.non_terminals)

                # Mais de 1 não-terminal
                if non_terminals_count > 1:
                    print(f"❌ {nt} → {prod} tem múltiplos não-terminais.")
                    problems = True

                # Não-terminal fora da última posição
                if non_terminals_count == 1:
                    if prod[-1] not in self.non_terminals:
                        print(f"❌ {nt} → {prod} não é linear à direita.")
                        problems = True

                # Produção muito longa
                if len(prod) > 2:
                    print(f"❌ {nt} → {prod} tem mais de 2 símbolos.")
                    problems = True

        if not problems:
            print("✅ Nenhum problema estrutural encontrado.")

        print("\n====================================\n")

    def generate_recognizer_pseudocode(self):
        print("\n====================================")
        print("   PSEUDOCÓDIGO DO RECONHECEDOR")
        print("====================================\n")

        tipo = self.classify()

        if tipo == "GR":
            print("Reconhecedor para Gramática Regular:\n")
            print("estado ← símbolo inicial")
            print("para cada símbolo da palavra:")
            print("    se existe transição válida:")
            print("        atualiza estado")
            print("    senão:")
            print("        rejeita")
            print("se estado é final:")
            print("    aceita")
            print("senão:")
            print("    rejeita")

        else:
            print("Reconhecedor para Gramática Livre de Contexto:\n")
            print("função reconhece(w):")
            print("    inicia com símbolo inicial")
            print("    tenta aplicar produções recursivamente")
            print("    se gerar exatamente w:")
            print("        aceita")
            print("    senão:")
            print("        rejeita")

        print("\n====================================\n")
