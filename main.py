import os

from Grafo import GrafoMatrizAdjacencia
from algoritmo import BuscaLargura, AGMPrim


def carregar_grafo(nome_arquivo):
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

    # Formato com cabeçalho: num_vertices / 0|1 / arestas...
    header_possible = False
    if len(linhas) >= 2:
        try:
            num_vertices = int(linhas[0])
            ponderado = int(linhas[1]) == 1
            header_possible = True
        except ValueError:
            header_possible = False

    if header_possible:
        edges = linhas[2:]
        if not edges:
            raise ValueError("Arquivo com cabeçalho deve conter arestas após a segunda linha.")
    else:
        edges = linhas
        linha_partes = [linha.split() for linha in edges]
        if all(len(partes) == 2 for partes in linha_partes):
            ponderado = False
        elif all(len(partes) == 3 for partes in linha_partes):
            ponderado = True
        else:
            raise ValueError(
                "Formato inválido. Use um arquivo com cabeçalho:\n"
                "1ª linha: número de vértices\n"
                "2ª linha: 0 ou 1\n"
                "ou apenas linhas de arestas: u v (não ponderado) ou u v peso (ponderado)"
            )

        max_vert = 0
        for partes in linha_partes:
            try:
                u, v = map(int, partes[:2])
            except ValueError:
                raise ValueError("Todas as arestas devem conter números inteiros.")
            max_vert = max(max_vert, u, v)

        if max_vert == 0:
            raise ValueError("Não foi possível inferir o número de vértices.")

        num_vertices = max_vert

    g = GrafoMatrizAdjacencia(num_vertices, ponderado)
    for indice, linha in enumerate(edges, start=(3 if header_possible else 1)):
        partes = linha.split()
        if ponderado:
            if len(partes) != 3:
                raise ValueError(f"Linha {indice}: esperam-se 3 valores (u v peso).")
            u, v, peso = map(int, partes)
            g.adicionar_aresta(u, v, peso)
        else:
            if len(partes) != 2:
                raise ValueError(f"Linha {indice}: esperam-se 2 valores (u v).")
            u, v = map(int, partes)
            g.adicionar_aresta(u, v)
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