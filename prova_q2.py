from cvxpy import GLPK_MI, Maximize, Variable, Problem, Minimize, Parameter, Constant, sum
import numpy as np

def tomatesPLI(deliciosidade):
    # --- 1. Variaveis de decisão e constantes ---
    x = Variable(len(deliciosidade), boolean= True)
    y = Constant(value= deliciosidade)

    # --- 2. Restricoes ---
    restricoes = []
    
    for i in range(len(deliciosidade) - 1):
        restricoes.append(x[i] + x[i+1] <= 1)

    # --- 3. Resolucao ---
    objetivo = Maximize(y.T @ x)

    problema = Problem(objetivo, restricoes)

    problema.solve()

    if problema.status in ['optimal', 'optimal_inaccurate']:
        print('Melhor deliciosidade: ', problema.value)
        print('Esquema de plantio: ', x.value)

def tomatesPD(deliciosidade):
    # --- 1. Inicializacao de variáveis ---
    tamanhoSolucao = (len(deliciosidade) // 2) + (len(deliciosidade) % 2)

    # solucao = np.zeros(shape= ((tamanhoSolucao + 1),len(deliciosidade)))
    solucao = np.full(shape= ((tamanhoSolucao + 1),len(deliciosidade)), fill_value= 10*len(deliciosidade), dtype= int)

    solucao[0,0] = deliciosidade[0]
    solucao[1,0] = 0

    solucao[1,1] = np.argmax(deliciosidade[:2])
    solucao[0,1] = deliciosidade[int(solucao[1,1])]

    for index, item in enumerate(deliciosidade):
        if index > 1:
            alternativa_1 = item + solucao[0, index - 2]
            alternativa_2 = solucao[0,index - 1]
            solucao[0,index] = max(alternativa_1, alternativa_2)

            
            if solucao[0,index] == alternativa_1:
                solucao[1,index] = index
                for i in range(len(solucao)):
                    if i > 1:
                        solucao[i,index] = solucao[i-1,index-2]

            elif solucao[0,index] == alternativa_2:
                for i in range(len(solucao)):
                    if i:
                        solucao[i,index] = solucao[i,index-1]

            else:
                print('Deu merda em algum lugar')
        
                return 0

    plantio = [item for item in solucao[1:,-1] if item < 10*len(deliciosidade)]
    esquemaPlantio = np.zeros(shape= len(deliciosidade), dtype= int)

    for item in plantio:
        esquemaPlantio[item] = 1
        
    
    print('Melhor deliciosidade: ', solucao[0,-1])   
    print('Esquema de plantio: ',esquemaPlantio) 
    

T1 = [5,12,10,7,15,10,11,5,8,10]
T2 = [10,12,5,12,20,18,5,3,2,8]

print('\nResultado PLI para T1:')
tomatesPLI(T1)

print('\nResultado PLI para T2:')
tomatesPLI(T2)

print('\nResultado PD para T1:')
tomatesPD(T1)

print('\nResultado PD para T2:')
tomatesPD(T2)