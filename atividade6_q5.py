from cvxpy import Variable, Problem, Minimize, sum, GLPK_MI
import numpy as np

PAR     = 1
IMPAR   = 0.5

def fluxoMinimo(matrizArcos):
    nosOrigem   = matrizArcos[:, 0]
    nosDestino  = matrizArcos[:, 1]

    nosTotal = np.concatenate((nosOrigem, nosDestino))
    nosTotal = np.unique(nosTotal)
    nosTotal.sort()

    qtdNos      = len(nosTotal)
    qtdArcos    = len(matrizArcos)

    capacidade = matrizArcos[:, 2]
    
    A = np.zeros((qtdNos, qtdArcos))

    for j, (i, k, _, _) in enumerate(matrizArcos):
        if i != 90:
            index_i = 2 * (int(i) // 10) - (int(i) % 2)
        else:
            index_i = -1
        
        if k != 90:
            index_k = 2 * (int(k) // 10) - (int(k) % 2)
        else:
            index_k = -1

        A[index_i, j] = 1     # arco que sai do nó i
        A[index_k, j] = -1    # arco que chega no nó k
    
    c = np.zeros(qtdArcos)
    c[-1] = 1

    b = np.zeros(qtdNos)
    
    for k in range(2):
        for arco in matrizArcos:
            if arco[k] != 90:
                index_b = 2 * (arco[k] // 10) - (arco[k] % 2)
            else:
                index_b = -1

            if not k:
                b[index_b] += arco[3]
            else:
                b[index_b] -= arco[3]

    x = Variable(qtdArcos, integer= True)
    objetivo = Minimize(c @ x)
    restricoes = [
        A @ x == b,
        x >= 0,
        x <= capacidade
    ]

    problema = Problem(objetivo, restricoes)
    problema.solve()

    if problema.status in ['optimal', 'optimal_inaccurate']:
        fluxoExcedente = x.value
        fluxosMinimos = capacidade
        fluxoReal = fluxoExcedente + fluxosMinimos

        matrizFluxos = np.column_stack((matrizArcos[:, 0], matrizArcos[:, 1], fluxoReal))

        demandaMinima = 0
        for fluxo in matrizFluxos:
            if fluxo[0] == 0:
                demandaMinima += round(fluxo[2],0)

        print(f'Devem ser alocadas no mínimo {demandaMinima} salas')

    else:
        print('Não foi possível encontrar uma solução ótima')


# --- 1. Entrada do problema ---
# Dados da tabela no formato [id_reuniao, hora_inicio, hora_termino]
agenda = np.array([
    [1, 13, 13.5],
    [2, 18, 20],
    [3, 10, 11],
    [4, 16, 17],
    [5, 16, 19],
    [6, 12, 13],
    [7, 14, 17],
    [8, 11, 12]
])

'''
    --- 2. Criar matriz de arcos ---
    a) dois nós por reuniao, sendo um para inicio, outro para final
    b) arcos entre eles com capacidade 1 (uma sala por reuniao) e custo zero
    c) uma fonte de salas conectando todos os inicios de reuniao com capacidade 1 e custo zero
    d) um dreno de salas conectado a todos os finais de reuniao com capacidade 1 e custo zero
    e) arco de retorno com capacidade infinita e custo 1
    f) verificar quais finais de reuniao podem se ligar a inicios de outras, a depender do tempo disponivel entre o horario final dessa e inicio da aroxima (cap1, custo0)
    g) matriz no formato [origem, destino, capacidade, custo]
'''

qtdReunioes = len(agenda)

arcos = []

# --- Criando os arcos entre inicio e final ---
for reuniao in agenda:
    idReuniao = reuniao[0]

    inicioReuniao   = (idReuniao * 10) + 1
    finalReuniao    = (idReuniao * 10) + 2

    arcos.append([int(inicioReuniao), int(finalReuniao), 1, 0])

fonte = 0
dreno = 90
nosFonte = []
nosDreno = []

# --- Criando os arcos que saem da fonte e que chegam no dreno ---
for arco in arcos:
    noFonte = [fonte, int(arco[0]), 1, 0]
    noDreno = [int(arco[1]), dreno, 1, 0]

    nosFonte.append(noFonte)
    nosDreno.append(noDreno)

arcos = np.vstack((arcos, nosFonte))
arcos = np.vstack((arcos, nosDreno))

# --- Criando os arcos entre salas ---
entreSalas = []

for i, reuniaoAtual in enumerate(agenda):
    for j, proximaReuniao in enumerate(agenda):
        if i != j:
            if int(proximaReuniao[0]) % 2:
                inicioProxima = proximaReuniao[1] - IMPAR
            else:
                inicioProxima = proximaReuniao[1] - PAR

            if reuniaoAtual[2] <= inicioProxima:
                arcoSala = [(int(reuniaoAtual[0]) * 10) + 2, (int(proximaReuniao[0]) * 10) + 1, 1, 0] 
                entreSalas.append(arcoSala)

arcos = np.vstack((arcos, entreSalas))

noRetorno = [90, 0, 1_000_000, 1]
arcos = np.vstack((arcos, noRetorno))

fluxoMinimo(arcos)