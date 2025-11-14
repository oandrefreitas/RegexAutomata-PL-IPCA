import json
import argparse

def fecho_epsilon(states, delta):
    """Calcula o fecho-epsilon de um conjunto de estados."""
    fecho = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        if "ε" in delta.get(state, {}):
            for novo_estado in delta[state]["ε"]:
                if novo_estado not in fecho:
                    fecho.add(novo_estado)
                    stack.append(novo_estado)
    return fecho

def transicao(estados, simbolo, delta):
    """Retorna conjunto de estados alcançáveis a partir de um conjunto de estados e um símbolo."""
    resultado = set()
    for estado in estados:
        resultado.update(delta.get(estado, {}).get(simbolo, []))
    return resultado

def nfa_para_dfa(nfa):
    """Converte um NFA em um DFA usando o método de construção de subconjuntos."""
    V = nfa["V"]
    Q = []
    delta = {}
    q0 = fecho_epsilon([nfa["q0"]], nfa["delta"])
    F = []
    fila = [q0]
    mapa_estados_dfa = {tuple(q0): "q0"}  # Usamos tupla como chave do dicionário
    while fila:
        estados_atuais = fila.pop(0)
        estado_dfa_atual = mapa_estados_dfa[tuple(estados_atuais)]
        Q.append(estado_dfa_atual)
        for simbolo in V:
            proximos_estados = fecho_epsilon(transicao(estados_atuais, simbolo, nfa["delta"]), nfa["delta"])
            if proximos_estados:
                chave_proximos_estados = tuple(proximos_estados)
                if chave_proximos_estados not in mapa_estados_dfa:
                    fila.append(proximos_estados)
                    mapa_estados_dfa[chave_proximos_estados] = "q" + str(len(mapa_estados_dfa))
                delta.setdefault(estado_dfa_atual, {})[simbolo] = mapa_estados_dfa[chave_proximos_estados]
        if any(estado in nfa["F"] for estado in estados_atuais):
            F.append(estado_dfa_atual)
    return {"V": V, "Q": Q, "delta": delta, "q0": "q0", "F": F}

def main():
    parser = argparse.ArgumentParser(description='Converter NFA to DFA')
    parser.add_argument('input', help='Input file with NFA in JSON format')
    parser.add_argument('-output', help='Output file for the DFA in JSON format', default='dfa_output.json')
    args = parser.parse_args()

    try:
        with open(args.input, "r") as f:
            nfa = json.load(f)
    except Exception as e:
        print(f"Failed to read the NFA file: {e}")
        return

    dfa = nfa_para_dfa(nfa)

    try:
        with open(args.output, "w") as f:
            json.dump(dfa, f, indent=2)
    except Exception as e:
        print(f"Failed to write the DFA file: {e}")

if __name__ == "__main__":
    main()