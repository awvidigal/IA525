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

    # --- 2.1. Restricao de unicidade ---
    # soma ao longo das colunas deve ser 1
    # soma ao longo das linhas deve ser 0 ou 1
    restricoes.extend([
        sum(matrizSolucao, axis= 0) <= 1,
        sum(matrizSolucao, axis= 0) >= 0,
        sum(matrizSolucao, axis= 1) == 1
    ])

    # --- 2.2. Restricao de existencia ---
    # Olhando para a coluna referente a cada valor da dica, a soma dos valores das 3 colunas deve ser igual ao numero de acertos naquela dica
    for i in range(len(matrizEntrada)):
        restricoes.append(
            sum(matrizSolucao[:, int(matrizDicas[i,0].value)]) +
            sum(matrizSolucao[:, int(matrizDicas[i,1].value)]) +
            sum(matrizSolucao[:, int(matrizDicas[i,2].value)]) == int(matrizDicas[i,3].value)
        )

    # --- 2.3. Restrição de posição ---
    for i in range(len(matrizEntrada)):
        # coluna 4 é uma flag que indica se odos os acertos da dica estao nos lugares corretos
        # se ela é 1, então a soma dos valores na matriz solução, nas células correspondentes aos digitos da dica na posição específica, deve ser igual ao numero de acertos
        # se for 0, então a soma desses valores deve ser maior ou igual a zero e menor do que a quantidade de acertos
        
        # restricao ativada quando a flag for 1
        restricoes.append(
            matrizSolucao[0, int(matrizDicas[i,0].value)]   +
            matrizSolucao[1, int(matrizDicas[i,1].value)]   +
            matrizSolucao[2, int(matrizDicas[i,2].value)]   -
            int(matrizDicas[i, 3].value)                    <= 100 * (1 - int(matrizDicas[i, 4].value))
        )

        # força o resultado da desigualdade para zero quando a flag é 1
        restricoes.append(
                             -
            matrizSolucao[0, int(matrizDicas[i,0].value)]   +
            matrizSolucao[1, int(matrizDicas[i,1].value)]   +
            matrizSolucao[2, int(matrizDicas[i,2].value)]   -
            int(matrizDicas[i, 3].value)                    >= -100 * (1 - int(matrizDicas[i, 4].value))
        )

        # restricao ativada quando a flag é 0
        restricoes.append(
            matrizSolucao[0, int(matrizDicas[i,0].value)]   +
            matrizSolucao[1, int(matrizDicas[i,1].value)]   +
            matrizSolucao[2, int(matrizDicas[i,2].value)]   -
            int(matrizDicas[i, 3].value)                    <= 100 * int(matrizDicas[i, 4].value) + 1
        )

        # soma de todos os valores da matriz solucao deve obrigatoriamente ser igual a 3
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

    else:
        print('Não foi possível encontrar solução para o problema')


entrada = np.array([
    [7,9,3,1,1],
    [7,2,5,1,0],
    [3,1,7,2,0],
    [8,4,9,0,0],
    [8,9,1,1,0]
])

'''
# --- Teste de entrada com dicas conflitantes ---
entrada = np.array([
    [7,9,3,1,1],
    [7,2,5,1,0],
    [3,1,7,2,0],
    [8,4,9,2,2],
    [8,9,1,1,0]
])

# --- Teste de entrada com dicas insuficientes ---
entrada = np.array([
    [7,9,3,1,1],
    [7,2,5,1,0]
])

'''

senha(entrada)