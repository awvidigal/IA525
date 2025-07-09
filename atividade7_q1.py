from cvxpy import GLPK_MI, Variable, Problem, Minimize, Parameter, Constant, sum
import numpy as np

'''
    A abordagem para resolução consistiu em:
    - minimizar a soma dos elementos da matriz solução
    - montar as restrições de maneira a garantir que cada célula tenha sido alterada uma quantidade par ou ímpar de vezes da seguinte forma:
        - par, se o valor inicial da célula na matriz de entrada for 1
        - ímpar, c.c.
'''

def resolveJogoPB(jogo):
    # --- 1. Recebe a matriz com o jogo montado, de qualquer tamanho ---
    matrizSolucao = Variable(shape= jogo.shape, boolean= True)
    linhas, colunas = matrizSolucao.shape

    # --- 2. Criando as variáveis para o solver ---
    matrizJogo              = Parameter(shape= jogo.shape, boolean= True)   # cria matrizJogo como um parâmetro que recebe os valores iniciais da matriz de entrada
    matrizAuxiliar          = Variable(shape= jogo.shape, integer= True)    # cria uma matriz cujos valores serão usados para criar a restrição que verifica se um valor é ímpar
    matrizJogo.value        = jogo  
    matrizSomaAlteracoes    = Variable(shape= jogo.shape)                   # cria a matrizSomaAlterações, cujos valores serão a quantidade de vezes que uma casa foi alterada
    
    objetivo = Minimize(sum(matrizSolucao))     # objetivo é minimizar a soma dos elementos da matrizSolucao, garantindo a menor quantidade de apertos possível
    
    # --- 3. Montando as restrições ---
    restricoes = []

    for linha in range(linhas):
        for coluna in range(colunas):
            # --- 3.1 Restrição que garante que todos os valores da matrizSolução serão 1 ---
            # cada elemento da matrizSolucao somado ao respectivo elemento da matriz de entrada deve ser ímpar 
            restricoes.append(matrizJogo[linha][coluna] + matrizSomaAlteracoes[linha][coluna] == 2 * matrizAuxiliar[linha][coluna] + 1)
            
            # --- 3.2 Restrição que monta a matrizSomaAlteracoes ---
            # seus elementos são formados pela soma dos valores da sua respectiva e das vizinhas diretas na matrizSolucao
            restricoes.append(
                matrizSomaAlteracoes[linha][coluna] == 
                matrizSolucao[linha][coluna] + 
                (matrizSolucao[linha - 1][coluna] if linha > 0 else 0) +
                (matrizSolucao[linha + 1][coluna] if linha < linhas - 1 else 0) +
                (matrizSolucao[linha][coluna - 1] if coluna > 0 else 0) +
                (matrizSolucao[linha][coluna + 1] if coluna < colunas - 1 else 0)
            )

            # --- 3.3 Define os limites para os elementos da matrizAuxiliar ---
            restricoes.append(matrizAuxiliar[linha][coluna] >= 0)   # elemento deve ser positivo
            restricoes.append(matrizAuxiliar[linha][coluna] <= 2)   # limita o elemento a um valor que garanta que o maior valor de uma somanão seja superior a 5

    problema = Problem(objetivo, restricoes)

    problema.solve(GLPK_MI)

    if problema.status in ['optimal', 'optimal_inaccurate']:
        print('Solução do problema:')
        print(matrizSolucao.value)

entrada = np.array([
    [1,0,1,1,1],
    [1,0,1,0,1],
    [0,0,1,0,0],
    [1,0,0,1,1],
    [0,1,0,1,0],
    [1,1,0,1,0]
])

resolveJogoPB(entrada)

