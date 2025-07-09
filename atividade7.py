from cvxpy import GLPK_MI, Variable, Problem, Minimize, Parameter, Constant, sum
import numpy as np

def resolveJogoPB(jogo):
    
    # --- 1. Recebe a matriz com o jogo montado, de qualquer tamanho ---
    matrizSolucao = Variable(shape= jogo.shape, boolean= True)
    linhas, colunas = matrizSolucao.shape

    print(matrizSolucao.shape)

    # --- 2. Criando as variáveis para o solver ---
    matrizJogo              = Parameter(shape= jogo.shape, boolean= True)
    matrizAuxiliar          = Variable(shape= jogo.shape, integer= True)
    matrizJogo.value        = jogo
    matrizSomaAlteracoes    = Variable(shape= jogo.shape)
    
    objetivo = Minimize(sum(matrizSolucao))
    
    # --- 3. Montando as restrições ---
    restricoes = []

    for linha in range(linhas):
        for coluna in range(colunas):
            restricoes.append(matrizJogo[linha][coluna] + matrizSomaAlteracoes[linha][coluna] == 2 * matrizAuxiliar[linha][coluna] + 1)
            restricoes.append(
                matrizSomaAlteracoes[linha][coluna] == 
                matrizSolucao[linha][coluna] + 
                (matrizSolucao[linha - 1][coluna] if linha > 0 else 0) +
                (matrizSolucao[linha + 1][coluna] if linha < linhas - 1 else 0) +
                (matrizSolucao[linha][coluna - 1] if coluna > 0 else 0) +
                (matrizSolucao[linha][coluna + 1] if coluna < colunas - 1 else 0)
            )

            restricoes.append(matrizAuxiliar[linha][coluna] >= 0)
            restricoes.append(matrizAuxiliar[linha][coluna] <= 2)

    problema = Problem(objetivo, restricoes)

    problema.solve(GLPK_MI)

    if problema.status in ['optimal', 'optimal_inaccurate']:
        print('Solução do problema: vvvvvvvvvv')
        print(matrizSolucao.value)
        print('Matriz de somas:')
        print(matrizSomaAlteracoes.value)
        print('Matriz k')
        print(matrizAuxiliar.value)

# entrada = np.array([
#     [1, 0, 0],
#     [1, 1, 1],
#     [0, 1, 0]
# ])

entrada = np.array([
    [1,0,1,1,1],
    [1,0,1,0,1],
    [0,0,1,0,0],
    [1,0,0,1,1],
    [0,1,0,1,0],
    [1,1,0,1,0]
])
resolveJogoPB(entrada)

