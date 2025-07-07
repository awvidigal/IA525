# import cvxpy as cp
import numpy as np

PAR     = 1
IMPAR   = 0.5

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

# --- 2. Criar matriz de arcos ---
# a) dois nós por reuniao, sendo um para inicio, outro para final
# b) arcos entre eles com capacidade 1 (uma sala por reuniao) e custo zero
# c) uma fonte de salas conectando todos os inicios de reuniao com capacidade 1 e custo zero
# d) um dreno de salas conectado a todos os finais de reuniao com capacidade 1 e custo zero
# e) arco de retorno com capacidade infinita e custo 1
# f) verificar quais finais de reuniao podem se ligar a inicios de outras, a depender do tempo disponivel entre o horario final dessa e inicio da aroxima (cap1, custo0)
# g) matriz no formato [origem, destino, capacidade, custo]

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

pass