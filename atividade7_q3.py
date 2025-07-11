from tabnanny import verbose
from cvxpy import GLPK_MI, Objective, Variable, Problem, Minimize, Parameter, Constant, sum, diag
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
    matrizDicas     = Constant(matrizEntrada)

    
    # --- 2. Definindo as restricoes ---
    restricoes = []

    '''
    restricoes:
    -> unicidade. nao há algarismos repetidos. soma dos elementos em cada coluna nao deve exceder 1
    
    '''
    # --- 2.1. Restricao de unicidade ---
    restricoes.extend([
        sum(matrizSolucao, axis= 0) <= 1,
        sum(matrizSolucao, axis= 0) >= 0,
        sum(matrizSolucao, axis= 1) == 1
    ])

    # --- 2.2. Restricao de existencia ---
    # identifica os valores que existem, independente da posição
    for i in range(len(matrizEntrada)):
        restricoes.append(
            sum(matrizSolucao[:, int(matrizDicas[i,0].value)]) +
            sum(matrizSolucao[:, int(matrizDicas[i,1].value)]) +
            sum(matrizSolucao[:, int(matrizDicas[i,2].value)]) == int(matrizDicas[i,3].value)
        )

    # --- 2.3. Restrição de posição ---
    for i in range(len(matrizEntrada)):
        # se flag, soma deve ser igual ao numero de acertos ->  soma - acertos == M*(1-flag)
        # se not flag, soma deve ser menor do que os acertos -> soma - acertos < flag*M
        
        restricoes.append(
            matrizSolucao[0, int(matrizDicas[i,0].value)]   +
            matrizSolucao[1, int(matrizDicas[i,1].value)]   +
            matrizSolucao[2, int(matrizDicas[i,2].value)]   -
            int(matrizDicas[i, 3].value)                    <= 100 * (1 - int(matrizDicas[i, 4].value))
        )

        restricoes.append(
                             -
            matrizSolucao[0, int(matrizDicas[i,0].value)]   +
            matrizSolucao[1, int(matrizDicas[i,1].value)]   +
            matrizSolucao[2, int(matrizDicas[i,2].value)]   -
            int(matrizDicas[i, 3].value)                    >= -100 * (1 - int(matrizDicas[i, 4].value))
        )

        restricoes.append(
            matrizSolucao[0, int(matrizDicas[i,0].value)]   +
            matrizSolucao[1, int(matrizDicas[i,1].value)]   +
            matrizSolucao[2, int(matrizDicas[i,2].value)]   -
            int(matrizDicas[i, 3].value)                    <= 100 * int(matrizDicas[i, 4].value) + 1
        )

        restricoes.append(sum(matrizSolucao) == 3)

    # --- 3. Resolvendo o problema ---
    objetivo = Minimize(1)
    problema = Problem(objetivo, restricoes)

    problema.solve(GLPK_MI, verbose= True)

    if problema.status in ['optimal', 'optimal_inaccurate']:
        senhaDecifrada = [0,0,0]
        
        for index, item in np.ndenumerate(matrizSolucao.value):
            if item:
                senhaDecifrada[index[0]] = index[1]
            
        print(f'A senha é: {senhaDecifrada}')


entrada = np.array([
    [7,9,3,1,1],
    [7,2,5,1,0],
    [3,1,7,2,0],
    [8,4,9,0,0],
    [8,9,1,1,0]
])

# entrada = np.array([
#     [1,2,3,3,1]
# ])

senha(entrada)