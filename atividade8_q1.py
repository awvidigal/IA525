from cvxpy      import GLPK_MI, Objective, Variable, Problem, Minimize, Parameter, Constant, sum as cp_sum, multiply as cp_multiply, diag
from tabnanny   import verbose

import numpy as np

# ['CLARABEL', 'CVXOPT', 'GLPK', 'GLPK_MI', 'OSQP', 'SCIPY', 'SCS']

COBERTURA = 0

def resolveAtribuicao(qtd, k):
    np.random.seed(42)
    c = np.random.randint(low= 0, high= 100, size= (qtd,qtd))
    
    print('\nCustos antes da atribuicao:',c)
    matrizSolucao = Variable(shape= (qtd,qtd))
    custos = Parameter(shape= (qtd,qtd), value= c)

    restricoes = []
    
    for i in range(qtd):
        # restricoes.append(cp_sum(matrizSolucao[:,i]) == 1)
        restricoes.append(cp_sum(matrizSolucao[i,:]) == 1)
        

    for j in range(qtd):
        restricoes.append(cp_sum(matrizSolucao[:,j]) == 1)

    if COBERTURA:
        for i in range(qtd):
            restricoes.append(cp_sum(diag(matrizSolucao)) >= k)

    objetivo = Minimize(cp_sum(cp_multiply(custos,matrizSolucao)))

    problema = Problem(objetivo, restricoes)

    problema.solve(verbose= True)

    if problema.status in ['optimal','optimal_inaccurate']:
        print('\nMatriz de custos:\n', custos.value)
        print('\nMatriz Solucao:\n',matrizSolucao.value)
        print('\nCusto total:\n',problema.value)

resolveAtribuicao(5, 0)