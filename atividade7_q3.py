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
    # auxiliarBinaria = Variable(shape= 1, boolean= True)
    verificaPosicao = Variable(shape= 10, boolean=True)

    matrizDicas.value = matrizEntrada
    
    # --- 2. Definindo as restricoes ---
    restricoes = []

    '''
    restricoes:
    -> unicidade. nao há algarismos repetidos. soma dos elementos em cada coluna nao deve exceder 1
    
    '''
    # --- 2.1. Restricao de unicidade ---
    restricoes.append([
        sum(matrizSolucao, axis= 0) <= 1,
        sum(matrizSolucao, axis= 1) == 1
    ])

    # --- 2.2. Restricao de posicao ---
    # se a variavel existe, só pode estar em uma posicao
    restricoes.append([
        verificaPosicao == sum(matrizSolucao[1:], axis= 0),
        matrizSolucao[0,:] == verificaPosicao
    ])



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