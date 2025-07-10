from re import M
from typing import List
import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

TIPO = 'quadrada'

def recuperarSinalQuadradosMinimos(tradeOff, x):
    """
    Recupera o sinal original a partir do trade-off, da matriz D, do vetor u e do vetor b.
    
    Parâmetros:
    -----------
    tradeOff (float): O trade-off entre a suavização e a fidelidade ao sinal original.
    x (np.ndarray): O sinal sujo.

    Retorna:
    --------
    np.ndarray: O sinal recuperado.
    """
    # Definindo as matrizes A, b e D
    x = x.reshape(-1, 1)  # Garantindo que x seja uma coluna

    m = x.shape[0]
    
    D = np.zeros((m, m))
    
    for j in range(m):
        for i in range(m):
            if i == j:
                if i != 1 and i != m:
                    D[i, j] = 2

                else:
                    D[i, j] = 1

            elif abs(j - i) == 1:
                D[i, j] = -1

    I = np.eye(m)
 
    A = cp.vstack([I, tradeOff * D])
  
    b = cp.vstack([x, np.zeros(D.shape[0]).reshape((-1, 1))])
 
    # Definindo a variável de otimização
    u = cp.Variable(m).reshape((-1, 1))
    
    # Definindo a função objetivo
    objective = cp.Minimize(cp.norm(A @ u - b, 2))
    
    # Definindo o problema
    problem = cp.Problem(objective)
    
    # Resolvendo o problema
    problem.solve()
    
    # return u.value.flatten()

    if problem.status == cp.OPTIMAL or problem.status == cp.OPTIMAL_INACCURATE:
        if u.value is not None: # Esta verificação explícita pode ajudar o linter
            return np.squeeze(u.value)
        else:
            # Caso extremo de u.value ser None mesmo com status OPTIMAL (muito improvável)
            print("Atenção: u.value é None mesmo com status OPTIMAL/OPTIMAL_INACCURATE. Retornando zeros.")
            return np.zeros(m)
    else:
        # Lógica para tratar o caso de falha, por exemplo, imprimir uma mensagem
        print(f"Problema CVXPY não foi resolvido com sucesso. Status: {problem.status}")
        return np.zeros(m) # Retorna um array de zeros ou levanta uma exceção, etc.


def recuperarSinalLASSO(tradeOff, x):
    x = x.reshape(-1, 1)  # Garantindo que x seja uma coluna
    print("Tamanho de x: ", x.shape)
    
    m = x.shape[0]

    # Criando as variáveis de decisão
    u = cp.Variable(m)

    # Criando a matriz D
    D = np.zeros((m, m))
    
    for j in range(m):
        for i in range(m):
            if i == j:
                if i != 1 or i != m:
                    D[i, j] = 2

                else:
                    D[i, j] = 1

            elif abs(j - i) == 1:
                D[i, j] = -1

    objective = cp.Minimize(cp.sum_squares(u-x)+(tradeOff * cp.norm(D @ u,1)))

    problem = cp.Problem(objective)
    problem.solve()

    if problem.status == cp.OPTIMAL or problem.status == cp.OPTIMAL_INACCURATE:
        if u.value is not None: # Esta verificação explícita pode ajudar o linter
            return np.squeeze(u.value)
        else:
            # Caso extremo de u.value ser None mesmo com status OPTIMAL (muito improvável)
            print("Atenção: u.value é None mesmo com status OPTIMAL/OPTIMAL_INACCURATE. Retornando zeros.")
            return np.zeros(m)
    else:
        # Lógica para tratar o caso de falha, por exemplo, imprimir uma mensagem
        print(f"Problema CVXPY não foi resolvido com sucesso. Status: {problem.status}")
        return np.zeros(m) # Retorna um array de zeros ou levanta uma exceção, etc.


# Parâmetros do ruído
media = 0
variancia = 0.01
desvioPadrao = np.sqrt(variancia)
amostragem = 1000

# Gerando o ruido
ruido = np.random.normal(media, desvioPadrao, amostragem)

# Onda senoidal
# Gerando o sinal original
ondaSenoidal = np.square(np.linspace(0, 20, amostragem))

# Onda quadrada
# Parâmetros do sinal
frequencia = 1  # Hz
discretizacao = 100 # Pontos por ciclo
duracao = 10     # Segundos
num_amostras = int(discretizacao * duracao)

# Eixo do tempo
tempo = np.linspace(0, duracao, num_amostras, endpoint=False)

# Gerar um sinal seno e aplicar np.sign para obter o sinal quadrado
sinal_seno = np.sin(2 * np.pi * frequencia * tempo)
ondaQuadrada = np.sign(sinal_seno)

if TIPO == 'quadrada':
    x = ondaQuadrada
else:
    x = ondaSenoidal

# Adicionando ruído ao sinal
xc = x + ruido

sinalOriginal = recuperarSinalLASSO(0.5, xc)

plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(x, '-')
plt.title('Sinal Original (10 pontos)')
plt.grid(True)
plt.xticks(np.arange(amostragem))

plt.subplot(3, 1, 2)
plt.plot(xc, '-', color='green')
plt.title('Sinal com Ruído Adicionado')
plt.grid(True)
plt.xticks(np.arange(amostragem))

plt.subplot(3, 1, 3)
plt.plot(sinalOriginal, '-', color='red')
plt.title('Sinal Recuperado')
plt.grid(True)
plt.xticks(np.arange(amostragem))

plt.tight_layout()
plt.show()