from cvxpy import Variable, Problem, Objective, Minimize, sum
import numpy as np

# 1. DADOS DE ENTRADA
# ---------------------
# arcos = np.array([origem, destino, capacidade minima, capacidade maxima])
# 
# 2. GERAR DADOS DO PROBLEMA
# -----------------------------
# qtdColunas, qtdLinhas
# loop preenchendo com 1 e -1 a matriz de incidencia A, de acordo com a matriz de arcos
# 
# vetor de capacidades efetivas capMax - capMin para os arcos internos e infinito para o arco de retorno
# vetor de custos, 0 para todos os arcos e 1 para o arco de retorno 
# 

# --- 1. Dados de entrada ---
arcos = np.array([
    [1, 2, 2, 10],
    [1, 3, 1, 8],
    [2, 3, 0, 5],
    [2, 4, 3, 7],
    [3, 4, 4, 9]
])

# --- 2. Adequação da matriz de entrada ---
capacidadesMinimas = arcos[:,2]
capacidadesMaximas = arcos[:,3]

capacidadesEfetivas = capacidadesMaximas - capacidadesMinimas

arcosAuxiliar = np.column_stack((arcos[:,:2], capacidadesEfetivas))
arcoDeRetorno = [4, 1, 1_000_000]
arcosAuxiliar = np.vstack((arcosAuxiliar, arcoDeRetorno))

capacidadesEfetivas = arcosAuxiliar[:,2]

# --- 3. Matriz de incidência ---
nosDestino = arcos[:,1]

qtdNos      = nosDestino.max()
qtdArcos    = len(arcosAuxiliar)

A = np.zeros((qtdNos, qtdArcos))

for j, (i, k, _) in enumerate(arcosAuxiliar):
    A[i-1, j] = 1     # arco que sai do nó i
    A[k-1, j] = -1    # arco que chega no nó k

# --- 4. Vetor de custos e de balanço nos nós ---
c = np.zeros(qtdArcos)
c[-1] = 1

b = np.zeros(qtdNos)
for arco in arcos:
    b[arco[0]-1] += arco[2]
    b[arco[1]-1] -= arco[2]

# def fluxoMinimo(totalArcos, matrizIncidencia, custos, balancos, capacidades, fluxosMinimos):
#     A = matrizIncidencia
#     c = custos
#     b = balancos
#     x = Variable(totalArcos, integer=True)
    
#     objetivo = Minimize(sum(c @ x))

#     restricoes = [
#         A @ x == b,
#         x >= 0,
#         x <= capacidades
#     ]
    
#     problema = Problem(
#         objective= objetivo,
#         constraints= restricoes
#     )

#     problema.solve()

#     if problema.status in ['optimal', 'optimal_inaccurate']:


# --- 5. Variaveis de decisão ---
x = Variable(qtdArcos, integer= True)

# --- 6. Função objetivo ---
objetivo = Minimize(sum(c @ x))

# --- 7. Restrições ---
constraints = [
    A @ x == b,
    x >= 0,
    x <= capacidadesEfetivas
]

# --- 8. Resolução ---
problema = Problem(objective= objetivo, constraints= constraints)
problema.solve()

if problema.status in ['optimal', 'optimal_inaccurate']:
    fluxosMinimos   = arcos[:,2]
    fluxosMinimos   = np.append(fluxosMinimos, 0)
    fluxosReais     = fluxosMinimos + x.value
    
    arcosAuxiliar = np.column_stack((arcosAuxiliar, fluxosReais))
    
    fMin = 0
    for arco in arcosAuxiliar:
        if arco[0] == 1:
            fMin += arco[3]
        
    fMin = round(fMin,0)
    print(f'Fluxo mínimo que atende as restrições dos arcos: {fMin}')

else:
    print('Não foi possível encontrar a solução ótima')



