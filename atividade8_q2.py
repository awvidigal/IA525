from cvxpy      import GLPK_MI, Objective, Variable, Problem, Minimize, Parameter, Constant, sum as cp_sum, multiply as cp_multiply, diag

import numpy as np

M = 10_000
z = 0.000_1

def resolveHorario(disponibilidade):
    # --- 1. Defnindo as variaveis de decisão ---
    '''
        1. Função objetivo
            - Minimizar o custo de alocação de docentes, tendo como base a matriz de disponibilidade
            - Matriz disponibilidade tem custo zero para docentes com disponibilidade naquele dia e horario e custo 100, c.c.
        
        2. Restriçoes
            1.1. Restricoes de professores
                - Dois PTx e dois PEx por dia ou
                - Dois PTP no mesmo dia (portugues)
                - Para cada PTx, deve haver um PEx da mesma matéria no mesmo dia para a mesma turma
            
            1.2. Restricoes de monitores
                - Deve haver uma quantidade igual de monitores Mx por materia por turma (havrerão monitores sem atribuição)

        3. Variáveis e parâmetros
            3.1. Matriz de decisão horario, com horario[i,j,k] assumindo valores booleanos
                - i: docente
                - j: horario
                - k: turma
                - 1: docente i alocado no horario j com a turma k
                - 0: c.c.

            3.2. Matriz disponibilidade
                - Custo zero para docentes com disponibilidade naquele dia e horario
                - Custo 100, c.c.

            3.3. Variáveis auxiliares
                - Variáveis binárias para restricoes condicionais
                - M -> valor muito grande para análise de restriçoes condicionais
                - z -> valor muito próximo de zero para análise de restriçoes condicionais
            
    '''
    linhas, colunas = disponibilidade.shape
    
    horario = Variable(shape= (linhas, colunas), boolean= True)
    custos = Parameter(shape= (linhas, colunas), value = disponibilidade)

    # Variáveis utilizadas para ajudar a defiir as restricoes de um professor de teoria e um de exercicio por dia
    auxBinPTPE_1 = Variable(shape= (14, 1), boolean= True)
    auxBinPTPE_2 = Variable(shape= (14, 1), boolean= True)


    # --- 2. Definindo as restricoes ---
    restricoes = []

    for i in range(14):
        # um professor de teoria por dia, um professor de exercicio por dia
        if not i % 2:
            restricoes.append(cp_sum(horario[i:i+2,:] <= 1)) 
        
        # um professor de teoria e um de exercicio no mesmo dia    
        if i in [0,4,8]: 
            restricoes.extend([
                horario[i:i+4,:] <=  M * (1 - auxBinPTPE_1[i]),
                horario[i:i+4,:] >= -M * (1 - auxBinPTPE_1[i]),
                horario[i:i+4,:] <= 2 + M * (1 - auxBinPTPE_1[i]),
                horario[i:i+4,:] >= 2 - M * (1 - auxBinPTPE_1[i]),
                cp_sum([auxBinPTPE_1, auxBinPTPE_2]) == 1
            ])

        if i == 12:
            restricoes.append(sum(horario[i:i+2,:] ))

    pass