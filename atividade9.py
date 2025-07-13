import heapq

def heuristica(a, b):
    # a e b são tuplas (linha, coluna)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(labirinto, inicio, fim):
    linhas, colunas = len(labirinto), len(labirinto[0])

    # O conjunto de nós a serem descobertos que podem precisar ser (re-)expandidos.
    # Inicialmente, apenas o nó inicial é conhecido.
    # Isso geralmente é implementado como um min-heap ou fila de prioridade.
    open_set = []
    heapq.heappush(open_set, (0, inicio)) # (fScore, nó)

    # Para o nó n, cameFrom[n] é o nó que o precede imediatamente no caminho mais barato do início
    # até n conhecido atualmente.
    came_from = {}

    # Para o nó n, gScore[n] é o custo do caminho mais barato do início até n conhecido atualmente.
    g_score = { (r, c): float('inf') for r in range(linhas) for c in range(colunas) }
    g_score[inicio] = 0

    # Para o nó n, fScore[n] := gScore[n] + heuristica(n, fim). fScore[n] representa nossa melhor estimativa
    # atual de quão barato um caminho poderia ser do início ao fim se passasse por n.
    f_score = { (r, c): float('inf') for r in range(linhas) for c in range(colunas) }
    f_score[inicio] = heuristica(inicio, fim)

    while open_set:
        # current é o nó em open_set com o menor fScore[]
        # heapq.heappop remove e retorna o menor item da heap
        current_f, current = heapq.heappop(open_set)

        if current == fim:
            return reconstruir_caminho(came_from, current)

        # Remove current do open_set (já foi removido pelo heappop)

        # Direções possíveis: cima, baixo, esquerda, direita
        movimentos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in movimentos:
            neighbor = (current[0] + dr, current[1] + dc)

            # Verifica se o vizinho está dentro dos limites do labirinto
            if 0 <= neighbor[0] < linhas and 0 <= neighbor[1] < colunas:
                # Verifica se o vizinho não é uma parede
                if labirinto[neighbor[0]][neighbor[1]] == 1:
                    continue # É uma parede, ignore

                # d(current, neighbor) é o peso da aresta de current para neighbor
                # Como estamos em um labirinto, cada movimento tem custo 1
                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score[neighbor]:
                    # Este caminho para o vizinho é melhor que qualquer um anterior. Registre-o!
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristica(neighbor, fim)
                    
                    # Se o vizinho não estiver no open_set, adicione-o
                    # (verificamos se ele já não está com um fScore menor,
                    # o que significa que já foi processado ou está na fila com um caminho pior)
                    # No caso de um heap, podemos simplesmente adicionar, pois o heappop sempre pegará o menor.
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # Open set está vazio, mas o objetivo nunca foi alcançado
    return "Nenhum caminho encontrado"

def reconstruir_caminho(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1] # Retorna o caminho na ordem correta (do início ao fim)