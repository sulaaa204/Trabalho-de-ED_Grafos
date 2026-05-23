import math

class GrafoMatrizAdjacencia:
    def __init__(self, num_vertices, ponderado=False):
        self.num_vertices = num_vertices
        self.ponderado = ponderado
        self.num_arestas = 0
        self.matriz = [[math.inf] * num_vertices for _ in range(num_vertices)]
        for i in range(num_vertices):
            self.matriz[i][i] = 0

    def adicionar_aresta(self, u, v, peso=1):
        u_idx = u - 1
        v_idx = v - 1
        self.matriz[u_idx][v_idx] = peso
        self.matriz[v_idx][u_idx] = peso
        self.num_arestas += 1

    def obter_vizinhos(self, u):
        u_idx = u - 1
        return [i + 1 for i, peso in enumerate(self.matriz[u_idx]) if i != u_idx and peso != 0 and peso != math.inf]

    def obter_peso(self, u, v):
        return self.matriz[u - 1][v - 1]

    def __repr__(self):
        return f"GrafoMatrizAdjacencia(num_vertices={self.num_vertices}, ponderado={self.ponderado})"

