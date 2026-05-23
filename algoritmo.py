from collections import deque

class Busca:
    def __init__(self, grafo):
        self.grafo = grafo

class BuscaLargura(Busca):
    def executar(self, raiz):
        visitados = [False] * self.grafo.num_vertices
        resultado = []  # Lista de (nó, pai, nível)
        fila = deque([(raiz, None, 0)])  # (vértice, pai, nível)
        visitados[raiz - 1] = True

        while fila:
            u, pai, nivel = fila.popleft()
            resultado.append({"no": u, "pai": pai, "nível": nivel})

            for v in self.grafo.obter_vizinhos(u):
                if not visitados[v - 1]:
                    visitados[v - 1] = True
                    fila.append((v, u, nivel + 1))
        return resultado

class ArvoreGeradoraMinima:
    def __init__(self, grafo):
        self.grafo = grafo

class AGMPrim(ArvoreGeradoraMinima):
    def executar(self):
        num_v = self.grafo.num_vertices
        pesos = [float('inf')] * num_v
        pai = [None] * num_v
        na_mst = [False] * num_v
        pesos[0] = 0

        for _ in range(num_v):
            u = -1
            min_val = float('inf')
            for i in range(num_v):
                if not na_mst[i] and pesos[i] < min_val:
                    min_val = pesos[i]
                    u = i

            if u == -1:
                break

            na_mst[u] = True

            for v in self.grafo.obter_vizinhos(u + 1):
                if na_mst[v - 1]:
                    continue

                if hasattr(self.grafo, 'matriz'):
                    peso = self.grafo.matriz[u][v - 1]
                elif hasattr(self.grafo, 'obter_peso'):
                    peso = self.grafo.obter_peso(u + 1, v)
                else:
                    raise AttributeError("Grafo precisa expor 'matriz' ou 'obter_peso'.")

                if peso is None or peso == 0 or peso == float('inf'):
                    continue

                if peso < pesos[v - 1]:
                    pesos[v - 1] = peso
                    pai[v - 1] = u + 1

        return pai, pesos
