from cvxpy      import GLPK_MI, Objective, Variable, Problem, Minimize, Parameter, Constant, sum as cp_sum, diag
from tabnanny   import verbose

import numpy as np

COBERTURA = 0

def resolveAtribuicao(qtd, k):
    # np.random.seed(105)
    c = np.ones((qtd,qtd))
    c = c + (5_000 * np.eye(qtd))
    print('\nCustos antes da atribuicao:',c)
    matrizSolucao = Variable(shape= (qtd,qtd), boolean= True)
    custos = Parameter(shape= (qtd,qtd), value= c)

    restricoes = []
    
    for i in range(qtd):
        restricoes.append(cp_sum(matrizSolucao[:,i]) == 1)
        restricoes.append(cp_sum(matrizSolucao[i,:]) == 1)

    if COBERTURA:
        for i in range(qtd):
            restricoes.append(cp_sum(diag(matrizSolucao)) >= k)

    objetivo = Minimize(cp_sum(custos @ matrizSolucao))

    problema = Problem(objetivo, restricoes)

    problema.solve(verbose= True)

    if problema.status in ['optimal','optimal_inaccurate']:
        print('\nMatriz de custos: ', custos.value)
        print('\nMatriz Solucao',matrizSolucao.value)
        print('\nCusto total:',problema.value)


resolveAtribuicao(7, 6)