//******************************PORTUGUÊS******************************//

# RegexAutomata-PL-IPCA

Projeto académico desenvolvido na unidade curricular de Processamento de Linguagens, focado em linguagens regulares. Inclui um conjunto de scripts em Python para trabalhar com autómatos finitos e expressões regulares, permitindo reconhecer palavras num AFD, gerar grafos com Graphviz, converter expressões regulares em AFND e transformar AFND em AFD, utilizando ficheiros JSON como formato de entrada e saída.

## Funcionalidades principais

* Leitura da definição de um Autómato Finito Determinista (AFD) a partir de um ficheiro JSON, com representação gráfica em Graphviz.

* Reconhecimento de palavras num AFD, indicando o caminho de estados percorrido e o motivo de erro quando a palavra não é aceite (símbolo fora do alfabeto ou estado não final).

* Conversão de uma expressão regular, representada como árvore sintática em JSON (`exemplo01.er.json`, `exemplo02.er.json`, `exemplo03.er.json`), para um Autómato Finito Não Determinista (AFND) em formato JSON.

* Conversão de um AFND em AFD equivalente, aplicando o método de construção de subconjuntos (incluindo fecho-ε) e gerando o novo autómato em JSON.

* Utilização de ficheiros JSON de exemplo (`automatop.json`, `auto2.json`) para testar as diferentes fases (reconhecimento, conversão ER→AFND e AFND→AFD).

* Execução via linha de comandos com o módulo `argparse`, permitindo especificar ficheiros de entrada e ficheiros de saída.


//******************************ENGLISH******************************//

# RegexAutomata-PL-IPCA

Academic project developed for the Language Processing course, focused on regular languages. It consists of a set of Python scripts to work with finite automata and regular expressions, allowing word recognition on a DFA, graph generation with Graphviz, conversion from regular expressions to NFA, and transformation from NFA to DFA, using JSON files as input and output.

## Main Features

* Reading a Deterministic Finite Automaton (DFA) definition from a JSON file and generating its Graphviz representation.

* Word recognition on a DFA, showing the sequence of visited states and reporting the error cause when the word is not accepted (symbol outside the alphabet or non-final state).

* Conversion of a regular expression, represented as a JSON syntax tree (`exemplo01.er.json`, `exemplo02.er.json`, `exemplo03.er.json`), into a Non-deterministic Finite Automaton (NFA) in JSON format.

* Conversion from an NFA to an equivalent DFA using the subset construction method (including epsilon-closure) and outputting the new automaton as JSON.

* Use of example JSON files (`automatop.json`, `auto2.json`) to test the different stages (recognition, RE→NFA conversion and NFA→DFA conversion).

* Command-line execution using the `argparse` module, allowing configuration of input and output files.
