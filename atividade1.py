import numpy as np
import matplotlib.pyplot as plt


# Gera uma quantidade aleatória de n pontos distribuídos ao longo de um círculo de raio aleatório
def pointsPolygon(n):
    '''
        Gera um polígono convexo com n pontos aleatórios

        Parâmetros:
        -----------
        n : inteiro
            Quantidade de pontos do polígono

        Retorno:
        --------
        polygonPoints : vetor
            Lista de pontos do poligono
    '''
    # Limite superior do ângulo
    boundary = 2*np.pi
    
    # Limite superior do raio
    radius = np.random.uniform(
        high= 0.5,
        low= 0.01
    )

    # Gera n ângulos aleatórios
    angles = np.random.uniform(
        high= boundary,
        size= n
    )

    # Ordena os ângulos em ordem crescente
    angles = np.sort(angles)

    # Gera um vetor de pontos com n linhas e 2 colunas
    polygonPoints = np.zeros((n,2))

    # Gera os pontos do polígono a partir dos ângulos e do raio    
    for point in range(n):
        polygonPoints[point] = [0.5 + (radius * np.cos(angles[point])),0.5 + (radius * np.sin(angles[point]))]

    return polygonPoints


def plotPolygon(pPoints,k):
    '''
        Plota o polígono e os pontos aleatórios gerados

        Parâmetros:
        -----------
        pPoints : vetor
            Lista de pontos do poligono
        
        k : inteiro
            Quantidade de pontos aleatórios a serem gerados

        Retorno:
        --------
        aleatoryPoints : vetor
            Lista de pontos aleatórios gerados
    '''
    # Empilha o primeiro ponto no final do vetor para fechar o polígono
    polygonPoints = np.vstack([pPoints, pPoints[0]])
    
    # Gera k pontos aleatórios dentro de uma área de 1x1, onde o polígono está contido
    aleatoryPoints = np.random.uniform(low=0, high=1, size=(k,2))

    # Plota o polígono e os pontos aleatórios
    plt.plot(polygonPoints[:, 0], polygonPoints[:, 1], marker='o')
    plt.fill(polygonPoints[:, 0], polygonPoints[:, 1], alpha=0.3)
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.title("Polígono Convexo Aleatório")
    plt.scatter(aleatoryPoints[:,0], aleatoryPoints[:,1], marker='o', s=1)

    plt.show()

    return aleatoryPoints

def verificaPontos(points, polygon):
    ''' 
        Verificação da localização de cada ponto gerado aleatoriamente

        Parâmetros:
        -----------
        points : vetor
            Lista de pontos aleatórios gerados previamente
        
        polygon : vetor
            Lista de vértices do poligono
    '''
    
    
    
    # filtrar todos os pontos completamente a direita, a esquerda, acima e abaixo do poligono
    # identificar o vértice mais a direita e mais a esquerda (maior e menor x)
    # filtrar todos os pontos q estão mais a esquerda e mais a direita
    # fazero mesmo para o eixo y
    # cerificar se o ponto está sobre uma reta do poligono
    # verificar no eixo x, para a direita, se uma reta a parir do ponto cruza o poligono um numero impar de vezes
    # verificar no eixo y, para cima, se uma reta a partir do ponto cruza o poligono um numero impar de vezes
    # garantir que nas verificações de cruzamento, a reta não cruze o poligono em um vértice

    # Empilha o primeiro ponto no final do vetor para fechar o polígono
    polygonPoints = np.vstack([points, points[0]])
    
    # Cria um vetor com len(polygon) linhas e 2 colunas, onde uma coluna é o coeficiente angular e a outra é o coeficiente linear
    retas = np.zeros((len(points),2))

    # Gera os coeficientes angulares e lineares para cada reta
    for i in range(len(polygonPoints)-1):
        # Calcula o coeficiente angular
        m = (polygonPoints[i+1][1] - polygonPoints[i][1]) / (polygonPoints[i+1][0] - polygonPoints[i][0])
        
        # Calcula o coeficiente linear
        b = polygonPoints[i][1] - (m * polygonPoints[i][0])

        retas[i] = [m,b]
    
    # Cria um vetor de pontos fora do polígono
    pointsOut = np.zeros((len(points),2))

    # Cria um vetor de pontos dentro do polígono
    pointsIn = np.zeros((len(points),2))

    # Empilha o primeiro ponto no final do vetor para fechar o polígono
    polygonPoints = np.vstack([polygon, polygon[0]])
    
    # Pega o ponto mais a direita e mais a esquerda
    maxX = np.max(polygonPoints[:,0])
    minX = np.min(polygonPoints[:,0])

    # Pega o ponto mais acima e mais abaixo
    maxY = np.max(polygonPoints[:,1])
    minY = np.min(polygonPoints[:,1])
    
    for point in range(len(points)):
        # Verifica se o ponto está completamente fora do polígono, observando os vértices mais extremos
        if points[point][0] > maxX or points[point][0] < minX or points[point][1] > maxY or points[point][1] < minY:
            pointsOut[point] = points[point]
            # Apagar os pontos no vetor de origem
            # Reordenar para que não fiquem espaços vazios no vetor de origem

         
        else:
            # Verifica se o ponto está sobre uma aresta do polígono
            for reta in range(len(retas)):
                # Verifica se o ponto está sobre a reta
                if points[point][1] == (retas[reta][0] * points[point][0]) + retas[reta][1]:
                    pointsIn[point] = points[point]
                    # Apagar os pontos no vetor de origem
                    # Reordenar para que não fiquem espaços vazios no vetor de origem
                    break

                else:
                    # Verifica os cruzamentos em x
                    contador = 0
                    for reta in range(len(retas)):
                        # Verifica cruzamento em x
                        cruzamentoX = (points[point][1] - retas[reta][1]) / retas[reta][0]
                        if cruzamentoX > points[point][0]:
                            contador += 1
                    
                    if contador % 2 == 1:
                        pointsIn[point] = points[point]
                        # Apagar os pontos no vetor de origem
                        # Reordenar para que não fiquem espaços vazios no vetor de origem
                    else:
                        pointsOut[point] = points[point]
                        # Apagar os pontos no vetor de origem
                        # Reordenar para que não fiquem espaços vazios no vetor de origem
                   

polygon = pointsPolygon(4)
aleatory = plotPolygon(polygon,10000)

