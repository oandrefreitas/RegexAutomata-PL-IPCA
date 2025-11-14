import json
from graphviz import Digraph
import argparse

# Gerar grafo do Automato, Diagraph é fornecido pela biblioteca Graphviz
def criar_grafo(automato):
    dot = Digraph(comment='Automato')


   # 'none' para um node invisível, string vazia, utilizado para dar inicio ao autonomo
    dot.node('start', shape='none', label='') 
    # criar transição inicial
    dot.edge('start', automato["q0"], label='')

     # criar os estados
    for state in automato["delta"].keys():
        if state in automato["F"]:
            dot.node(state, state, shape="doublecircle")  # estado final
        else:
            dot.node(state, state, shape="circle")  # estado não final

 # criar as transições
    for estado_inicial, transitions in automato["delta"].items():
        for simbolo, estado_final in transitions.items():
            dot.edge(estado_inicial, estado_final, label=simbolo) # cria as arestas
            
    # visualização
    dot.render('Grafo', view=True, format='png')

     # obter a representação em formato de texto do digraph
    dot_text = dot.source

    # imprimir no terminal
    print(dot_text)


def reconhecer_palavra(palavra, automato):
    estado_inicial = automato["q0"]
    estados_finais = automato["F"]
    transicoes = automato["delta"]
    estado_atual = estado_inicial
    caminho = [estado_inicial]  # Lista para armazenar o caminho percorrido


    for char in palavra:
        if estado_atual not in transicoes or char not in transicoes[estado_atual]:
            print(f"\nErro: Símbolo '{char}' não pertence ao alfabeto da linguagem.")
            return

        estado_atual = transicoes[estado_atual][char]  # Atualiza o estado atual
        caminho.append(estado_atual)  # Adiciona o novo estado ao caminho percorrido

        print(f"{estado_atual}-{char} -> ", end="")  # Imprime o novo estado e o caractere lido

    # Verifica se o estado atual é um estado final após o loop
    if estado_atual in estados_finais:
        print(f"{estado_atual} (estado final).")
        print(f"A palavra '{palavra}' é reconhecida.")
    else:
        print(f"{estado_atual} (não é um estado final).")
        print(f"A palavra '{palavra}' não é reconhecida.")


def main():
    parser = argparse.ArgumentParser(description='Criar grafos')
    parser.add_argument('input', help='Arquivo JSON contendo a descrição do automato')
    parser.add_argument("-rec", type=str, help="Palavra a ser reconhecida")
    parser.add_argument('-graphviz', action='store_true', help='Gerar o grafo do automato')
    args = parser.parse_args()

  # Lê o arquivo JSON
    with open(args.input, "r", encoding="utf-8") as f:
        automato = json.load(f)


# -graphviz 
    if args.graphviz:
        criar_grafo(automato)
        

# reconhecer a palavra
    if args.rec:
        reconhecer_palavra(args.rec, automato)

if __name__ == '__main__':
    main()