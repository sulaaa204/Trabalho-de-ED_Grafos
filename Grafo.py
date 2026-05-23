import math

class GrafoMatrizAdjacencia:
    def __init__(self, num_vertices, ponderado=False):
        self.num_vertices = num_vertices
        self.ponderado = ponderado
        self.num_arestas = 0
        
        # Se for ponderado, posições vazias são Infinito. Se não, são 0.
        valor_inicial = math.inf if ponderado else 0
        self.matriz = [[valor_inicial] * num_vertices for _ in range(num_vertices)]
        
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
        vizinhos = []
        for i, peso in enumerate(self.matriz[u_idx]):
            if i != u_idx:  # Não é a diagonal principal
                if self.ponderado:
                    # No ponderado, vizinho válido não é INF e não é 0
                    if peso != math.inf and peso != 0:
                        vizinhos.append(i + 1)
                else:
                    # No NÃO ponderado, vizinho válido é quem tem conexão ativa (diferente de 0)
                    if peso != 0:
                        vizinhos.append(i + 1)
        return vizinhos

    def obter_peso(self, u, v):
        return self.matriz[u - 1][v - 1]

    def __repr__(self):
        return f"GrafoMatrizAdjacencia(num_vertices={self.num_vertices}, ponderado={self.ponderado})"

    def obter_peso(self, u, v):
        return self.matriz[u - 1][v - 1]

    def __repr__(self):
        return f"GrafoMatrizAdjacencia(num_vertices={self.num_vertices}, ponderado={self.ponderado})"

