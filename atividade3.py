from re import M
from typing import List
import cvxpy as cp
import numpy as np

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
    A = cp.vstack([i, tradeOff * D])
    b = cp.vstack([x, np.zeros(D.shape[0])])


    

    # Definindo a variável de otimização
    u = cp.Variable(shape= x.shape[1])
    
    # Definindo a função objetivo
    objective = cp.Minimize(cp.norm(A @ x - b, 2))
    
    # Definindo as restrições
    # constraints = [D @ x == b]
    
    # Definindo o problema
    problem = cp.Problem(objective)
    
    # Resolvendo o problema
    problem.solve()
    
    return u.value

def recuperarSinalLASSO(tradeOff, x):
    x = x.reshape(-1, 1)  # Garantindo que x seja uma coluna
    
    m = x.shape[0]

    # Criando as variáveis de decisão
    u = cp.Variable(m)
    t = cp.Variable(m)

    # Criando a matriz D
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
    
    # Matriz identidade que será usada para montar a matriz Q
    I = np.eye(m)

    # Matriz de uns que será utilizada para a matriz p
    ones = np.ones((m, 1))

    # Matrizes nulas que serão usadas para a matriz Q
    zero = np.zeros((m, m))

    # Criando a matriz Q
    Q = cp.bmat([
        [2 * cp.Constant(I), cp.Constant(zero)],
        [cp.Constant(zero), cp.Constant(zero)]
    ])

    # Criando o vetor p
    p = cp.vstack([-2 * x, tradeOff * ones])

    _x = cp.vstack([u.reshape((-1, 1)), t.reshape((-1, 1))])

    restr1 = cp.Constant(D) @ u <= t
    restr2 = -cp.Constant(D) @ u <= t
    restr3 = t >= 0

    objective = cp.Minimize(0.5 * (((_x.T) @ Q) @ _x) + p.T @ _x)
    constraints: List[cp.Constraint] = [restr1, restr2, restr3]
    
    problem = cp.Problem(objective, constraints)
    problem.solve()



tOff = input("Digite o valor do trade-off: ")
x = input("Insira as amostras do sinal corrompido separados por espaço: ")
x = np.array(x.split(), dtype=float).reshape(-1, 1)

sinalOriginal = recuperarSinalQuadradosMinimos(float(tOff), x)

print("\nSinal recuperado:", sinalOriginal)


