import json
import argparse


def construir_afnd(er_json):
    alfabeto = set() #conjunto de simbolos do alfabeto
    estados = set() #conjunto de estados do alfabeto
    transicoes = {} # Dicionario de transições
    estados_finais = set() # conjunto de estado do AFND

    contador_estados = 0

    #gerar o conjunto de estados de forma que sejam sempre valores diferentes
    def gerar_nome_estado():
        nonlocal contador_estados
        nome_estado = f"q{contador_estados}"
        contador_estados += 1
        return nome_estado

    #Recebe o node da arvore da ER em formato dicionario e o estado atual do AFND
    def percorrer(node, estado_atual):
        nonlocal alfabeto, estados, transicoes, estados_finais
        
        #percorre a arvore da ER para adicionar os simbolos ao conjunto alfabeto
        if isinstance(node, dict):
            if "simb" in node:
                alfabeto.add(node["simb"])  
                return

            if "op" in node:
                if node["op"] == "seq":
                    estado_anterior = estado_atual 
                    for idx, arg in enumerate(node["args"]): #idx | enumerate -permite obter o indice e o valor do elemento durante a iteração
                        novo_estado = gerar_nome_estado()
                        estados.add(novo_estado)
                        percorrer(arg, novo_estado)
                        # Garante que o valor de transição seja sempre uma string
                        if arg.get("simb"):
                            transicoes.setdefault(estado_anterior, {}).setdefault(arg["simb"], []).append(novo_estado) #verifica se existe um simbolo na transição
                        else:
                            transicoes.setdefault(estado_anterior, {}).setdefault("ε", []).append(novo_estado) #se for fazia
                        estado_anterior = novo_estado
                    estados_finais.add(novo_estado)

                # para criar duas opções alternativas
                elif node["op"] == "alt":
                    estado_esquerdo = gerar_nome_estado()
                    estado_direito = gerar_nome_estado()
                    estados.add(estado_esquerdo)
                    estados.add(estado_direito)

                    percorrer(node["args"][0], estado_esquerdo)
                    percorrer(node["args"][1], estado_direito)

                    transicoes[estado_atual] = {
                        "ε": [estado_esquerdo, estado_direito]
                    }

                #operação transição
                elif node["op"] == "trans":
                    estado_alvo = gerar_nome_estado()
                    estados.add(estado_alvo)
                    if node["args"][0].get("simb") is not None:
                        alfabeto.add(node["args"][0]["simb"])  # Adiciona o símbolo ao alfabeto
                        transicoes[estado_atual] = {
                            node["args"][0]["simb"]: estado_alvo
                        }
                elif "epsilon" in node["args"][0]:  # Verifica se há transição epsilon
                    #alfabeto.add("ε")  # Adiciona o epsilon ao alfabeto
                    transicoes[estado_atual] = {
                        "ε": estado_alvo
                    }

                #fecho kleen para lidar com repetição de zero ou de um padrão
                elif node["op"] == "kle":
                    novo_estado = gerar_nome_estado()
                    estados.add(novo_estado)
                    transicoes[estado_atual] = {node["args"][0].get("simb", "ε"): novo_estado}
                    transicoes[novo_estado] = {node["args"][0].get("simb", "ε"): novo_estado}
                    estados_finais.add(novo_estado)
                    percorrer(node["args"][0], novo_estado) # repetição de padrões internos

    estado_inicial = "q0"
    estados.add(estado_inicial) # adiciona o estado inicial ao conjunto de estados
    percorrer(er_json, estado_inicial) #ler a arvore

    return {
        "V": sorted(list(alfabeto)),  # Ordena o alfabeto
        "Q": sorted(list(estados)),
        "delta": transicoes,
        "q0": estado_inicial,
        "F": sorted(list(estados_finais))
    }

def ler_er_do_arquivo(caminho_arquivo):
    with open(caminho_arquivo, "r") as arquivo:
        er_json = json.load(arquivo)
    return er_json

def main():
    parser = argparse.ArgumentParser(description='Convertendo expressão regular para autômato finito não determinístico (AFND)')
    parser.add_argument('input', help='Arquivo JSON contendo a descrição da expressão regular')
    parser.add_argument('-output', help='Nome do arquivo JSON de saída para o AFND', required=True)
    args = parser.parse_args()

    er_json = ler_er_do_arquivo(args.input)
    afnd_json = construir_afnd(er_json)

    with open(args.output, "w") as afnd_file:
        json.dump(afnd_json, afnd_file, indent=4)


if __name__ == '__main__':
    main()