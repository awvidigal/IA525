from cvxpy import GLPK_MI, Variable, Problem, Minimize, Parameter, Constant, sum
import numpy as np

# matriz ordem n=3, i, j, k
#  i,j -> posições do sudoku
#  k -> valor a ser utilizado
def sudoku(jogoInicial):
    # --- 1. Montagem da matriz tridimensional a partir da entrada ---
    matrizConstrucao = np.zeros(shape= [9,9,9])

    for index, elemento in np.ndenumerate(jogoInicial):
        if jogoInicial[index[0]][index[1]] != 0:
                matrizConstrucao[index[0]][index[1]][elemento-1] = 1

# --- 2. Definicao das variáveis ---
    matrizInicio = Parameter(shape= [9,9,9])
    matrizInicio.value = matrizConstrucao

    metaArray = Constant(np.ones(9))

    matrizSolucao = Variable(shape= [9,9,9], boolean= True)

    # --- 3. Definição das restrições ---
    restricoes = []

    # --- 3.1 Restricao para forçar os valores iniciais iguais aos de entrada ---
    for index_i in range(9):
         for index_j in range(9):
              for index_k in range(9):
                   if matrizConstrucao[index_i, index_j, index_k] != 0:
                        restricoes.append(matrizSolucao[index_i, index_j, index_k] == 1)

    # --- 3.2 Restricao que garante que cada casa terá apenas um valor de 1 a 9 ---
    for index_i in range(9):
        for index_j in range(9):                
            restricoes.append(sum(matrizSolucao[index_i][index_j]) == 1)

    # --- 3.3 Restricao que garante que cada linha terá todos os valores de 1 a 9 ---
    for index_i in range(9):
        restricoes.append(sum(matrizSolucao[index_i], axis= 0) == metaArray)

    # --- 3.4 Restricao que garante que cada coluna terá todos os valores de 1 a 9 ---
    for index_j in range(9):
        restricoes.append(sum(matrizSolucao[:,index_j,:], axis= 0) == metaArray)

    # --- 3.5 Restricoes que garantem que dentro de cada subquadrado haverá os numeros de 1 a 9 ---
    for linha in [[0,3], [3,6], [6,9]]:
         for coluna in [[0,3], [3,6], [6,9]]:
              restricoes.append(sum(sum(matrizSolucao[linha[0]:linha[1], coluna[0]:coluna[1], :], axis= 0), axis= 0) == metaArray)

    
    objetivo = Minimize(1)

    problema = Problem(objetivo,restricoes)

    solucao = np.zeros([9,9])

    problema.solve(GLPK_MI)

    # print(matrizSolucao.value)
    
    if problema.status in ['optimal', 'optimal_inaccurate']:
        for index, elemento in np.ndenumerate(matrizSolucao.value):
            linha  = index[0]
            coluna = index[1]
            valor  = index[2]

            if elemento == 1:
                solucao[linha, coluna] = int(valor + 1) 
         
        print('yeeeeey')
        print(solucao)


entrada = np.array([
    [0,2,0,0,3,0,0,4,0],
    [6,0,0,0,0,0,0,0,3],
    [0,0,4,0,0,0,5,0,0],
    [0,0,0,8,0,6,0,0,0],
    [8,0,0,0,1,0,0,0,6],
    [0,0,0,7,0,5,0,0,0],
    [0,0,7,0,0,0,6,0,0],
    [4,0,0,0,0,0,0,0,8],
    [0,3,0,0,4,0,0,2,0],
])

sudoku(entrada)