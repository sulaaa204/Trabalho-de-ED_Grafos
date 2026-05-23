import os

from Grafo import GrafoMatrizAdjacencia
from algoritmo import BuscaLargura, AGMPrim


def carregar_grafo(nome_arquivo, ponderado_usuario=None):
    caminho = nome_arquivo
    if not os.path.isfile(caminho) and not caminho.lower().endswith('.txt'):
        caminho_txt = caminho + '.txt'
        if os.path.isfile(caminho_txt):
            caminho = caminho_txt

    if not os.path.isfile(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {nome_arquivo}")

    with open(caminho, 'r', encoding='utf-8-sig') as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    if not linhas:
        raise ValueError("O arquivo está vazio.")

    # Formato com cabeçalho:
    # - primeira linha: num_vertices [0(sem peso)|1(com peso)]
    # - segunda linha (opcional): 0|1 se o cabeçalho for curto.
    header_possible = False
    if len(linhas) >= 1:
        first_tokens = linhas[0].split()
        if len(first_tokens) >= 2:
            try:
                num_vertices = int(first_tokens[0])
                if ponderado_usuario is None:
                    ponderado = int(first_tokens[1]) == 1
                else:
                    ponderado = ponderado_usuario
                header_possible = True
                edges = linhas[1:]
            except ValueError:
                header_possible = False
        elif len(linhas) >= 2:
            try:
                num_vertices = int(linhas[0])
                second_tokens = linhas[1].split()
                if len(second_tokens) == 1 and second_tokens[0] in {'0', '1'}:
                    if ponderado_usuario is None:
                        ponderado = int(second_tokens[0]) == 1
                    else:
                        ponderado = ponderado_usuario
                    header_possible = True
                    edges = linhas[2:]
                else:
                    header_possible = False
            except ValueError:
                header_possible = False

    if not header_possible:
        # Se o arquivo não tem cabeçalho de 2 linhas, a primeira linha pode ser apenas o número de vértices,
        # ou pode não ter cabeçalho nenhum. Tentamos inferir o formato pelas linhas de arestas.
        num_vertices = int(linhas[0].split()[0])
        ponderado = ponderado if ponderado is not None else False
        edges = linhas[1:]

    g = GrafoMatrizAdjacencia(num_vertices, ponderado)
    
    for linha in edges:
        # Remove comentários se houverem no arquivo (ex: #aresta entre 1 e 2)
        linha_limpa = linha.split('#')[0].strip()
        if not linha_limpa:
            continue
            
        partes = linha_limpa.split()

        if len(partes) >= 2:
            u = int(partes[0])
            v = int(partes[1])

            # Se a terceira coluno existir, ela é o peso. Se não, assume peso 1 para grafos ponderados.
            if len(partes) >= 3:
                peso = float(partes[2])

                if not g.ponderado:
                    g.ponderado = True  # Se encontramos um peso, o grafo é ponderado
                
                g.adicionar_aresta(u, v, peso)
                
            else:
                g.adicionar_aresta(u, v, 1)
    return g



def menu():
    while True:
        arquivo = input("Digite o nome do arquivo do grafo: ")
        try:
            g = carregar_grafo(arquivo)
            break
        except FileNotFoundError as e:
            print(e)
        except ValueError as e:
            print("Erro ao ler arquivo:", e)

    while True:
        print("\n1. Info() | 2. Print() | 3. Busca(v) | 4. MST() | 0. Sair")
        opcao = input("Escolha: ")

        if opcao == '1':
            print(f"Vértices: {g.num_vertices}, Arestas: {g.num_arestas}")
            grau_medio = (2 * g.num_arestas) / g.num_vertices
            print(f"Grau Médio: {grau_medio:.2f}")

        elif opcao == '2':
            for i in range(1, g.num_vertices + 1):
                vizinhos = g.obter_vizinhos(i)
                print(f"{i}: {', '.join(map(str, vizinhos))}")

        elif opcao == '3':
            v = int(input("Vértice raiz: "))
            bfs = BuscaLargura(g)
            for res in bfs.executar(v):
                print(f"No {res['no']}; Pai {res['pai'] or 'x'}; Level {res['nível']}")

        elif opcao == '4':
            prim = AGMPrim(g)
            pais, pesos = prim.executar()
            peso_total = sum(p for p in pesos if p != float('inf'))
            print(f"Peso total: {peso_total}")
            for i, p in enumerate(pais):
                if p:
                    print(f"Aresta {p}-{i + 1}")

        elif opcao == '0':
            break


if __name__ == "__main__":
    menu()
