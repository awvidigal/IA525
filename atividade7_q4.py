from cvxpy import GLPK_MI, Variable, Problem, Minimize, Parameter, Constant, sum, diag
import numpy as np

'''
Assim como sudoku, não tem função objetivo. Deve respeitar as restrições apenas
-> soma das linhas deve ser um array de uns
-> soma das colunas deve ser um array de uns
-> soma das diagonais deve ser <= 1
-> inicial deve ser igual a matriz de entrada
'''
def rainhas(matrizJogo):
    # --- 1. Definição das variáveis ---
    matrizSolucao = Variable(shape= matrizJogo.shape, boolean= True)
    metaArray = Constant(np.ones(8))

    
    # --- 2. Definindo restrições ---
    # --- 2.1. Restricoes de linha e coluna ---
    restricoes = [
        sum(matrizSolucao, axis=0) == metaArray,
        sum(matrizSolucao, axis=1) == metaArray.T
    ]

    # --- 2.2. Restricao para matriz de entrada ---
    for index, elemento in np.ndenumerate(matrizJogo):
        if int(elemento) != 0:
            restricoes.append(matrizSolucao[index] == 1)

    # --- 2.3. Restricoes das diagonais
    restricoes.append(sum(diag(matrizSolucao)) <= 1)
    for k in range(7):
        restricoes.append(sum(diag(matrizSolucao, (k+1)))   <= 1)
        restricoes.append(sum(diag(matrizSolucao, -(k+1)))  <= 1)
        

    objetivo = Minimize(1)
    problema = Problem(objetivo,restricoes)
    problema.solve(GLPK_MI)

    if problema.status in ['optimal', 'optimal_inaccurate']:
        print('Solução do jogo da rainha:')
        print(matrizSolucao.value)


entrada = np.array([
    [0,0,0,0,0,1,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1],
    [0,1,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,1,0,0,0,0,0],
])

rainhas(entrada)