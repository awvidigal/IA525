from cvxpy import GLPK_MI, Variable, Problem, Minimize, Parameter, Constant, sum, diag
import numpy as np

'''
entrada: matriz de dicas
solucao = matriz(3,10)
-> colunas representam os valores possiveis [0:9]
-> pode assumir valores:    0 = não
                            1 = sim
-> linha 0: está na posicao 0?
-> linha 1: está na posicao 1?
-> linha 2: está na posição 2?
'''

def senha(matrizEntrada):
    # --- 1. Definindo as variaveis ---
    matrizSolucao   = Variable(shape= [3, 10], boolean= True)
    matrizDicas     = Constant(shape= matrizEntrada.shape)

    

    matrizDicas.value = matrizEntrada
    
    # --- 2. Definindo as restricoes ---
    restricoes = []

    '''
    restricoes:
    -> unicidade. nao há algarismos repetidos. soma dos elementos em cada coluna nao deve exceder 1
    
    '''
    # --- 2.1. Restricao de unicidade ---
    restricoes.extend([
        sum(matrizSolucao, axis= 0) <= 1,
        sum(matrizSolucao, axis= 1) == 1
    ])

    # --- 2.2. Restricao de existencia ---
    # identifica os valores que existem, independente da posição
    for i in range(len(matrizDicas)):
        restricoes.append(
            sum(matrizSolucao[:, matrizDicas[i,0]]) +
            sum(matrizSolucao[:, matrizDicas[i,1]]) +
            sum(matrizSolucao[:, matrizDicas[i,2]]) == matrizDicas[i,3]
        )

    # --- 2.3. Restrição de posição ---
    for i in range(len(matrizDicas)):
        # se flag, soma deve ser igual ao numero de acertos ->  soma - acertos == M*(1-flag)
        # se not flag, soma deve ser menor do que os acertos -> soma - acertos < flag*M
        
        restricoes.extend(
            sum(matrizSolucao[:, matrizDicas[i,:3]]) - matrizDicas[i,3] == 1_000 * (1 - matrizDicas[i, 4]),
            sum(matrizSolucao[:, matrizDicas[i,:3]]) - matrizDicas[i,3] < 1_000 * matrizDicas[i, 4]
        )



    # --- 3. Resolvendo o problema ---
    pass


entrada = np.array([
    [7,9,3,1,1],
    [7,2,5,1,0],
    [3,1,7,2,0],
    [8,4,9,0,0],
    [8,9,1,1,0]
])

senha(entrada)