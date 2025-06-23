# Algoritmo otimização de corte para barra de tamanho n
# Resolver para o caso base n=2
# Resolver para o caso base n=3 onde a melhor solução será n=2 + n=1 ou n=3
# Resolver para o caso base n=4 onde a melhor solução será n=3 + n=1 ou n=4

def calculaMelhorCorteMemo(n, precos, memo=None):
    '''
        Calcula o melhor corte para uma barra de tamanho n usando memoização.

        Parâmetros:
        -----------
        n : inteiro
            Tamanho da barra
        precos : vetor
            Lista de preços para cada tamanho de corte
        memo : dicionário
            Cache para armazenar resultados intermediários

        Retorno:
        --------
        melhorPreco : inteiro
            Melhor preço obtido para o corte da barra de tamanho n
        
        esquemaDeCorte : lista
            Vetor que representa o esquema de corte
    '''
    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n == 0:
        return 0, []

    melhorPreco = float('-inf')
    melhorEsquema = []

    for corte in range(1, n + 1):
        if corte <= len(precos):
            precoAtual, esquemaAtual = calculaMelhorCorteMemo(n - corte, precos, memo)
            precoAtual += precos[corte - 1]
            if precoAtual > melhorPreco:
                melhorPreco = precoAtual
                melhorEsquema = esquemaAtual + [corte]

    memo[n] = (melhorPreco, melhorEsquema)
    return memo[n]

def calculaMelhorCorte(n, precos):
    '''
        Calcula o melhor corte para uma barra de tamanho n

        Parâmetros:
        -----------
        n : inteiro
            Tamanho da barra
        precos : vetor
            Lista de preços para cada tamanho de corte

        Retorno:
        --------
        melhorPreco : inteiro
            Melhor preço obtido para o corte da barra de tamanho n
        
        esquemaDeCorte : inteiro
            Vetor que representa o esquema de corte
            Exemplo: [2, 1] significa que o corte foi feito em uma barra de tamanho 2 e uma barra de tamanho 1
    '''
    if len(precos) == 0 or len(precos) < n:
        raise ValueError("A lista de preços deve conter pelo menos n elementos.")
    
    melhorPreco = 0
    melhorEsquema = []

    if n == 0:
        # Caso base: barra de tamanho 0
        melhorPreco = 0
        melhorEsquema = []
        return melhorPreco, melhorEsquema
    
    else:
        for corte in range(1, n+1):
            precoAtual, esquemaAtual = calculaMelhorCorte(n-corte, precos)
            precoAtual += precos[corte-1]

            if precoAtual > melhorPreco:
                melhorPreco = precoAtual
                melhorEsquema = esquemaAtual + [corte]
       
        return melhorPreco, melhorEsquema
    
n = 17
precosBarra = [1, 2, 10, 22, 25, 32, 59, 68, 79, 92, 102, 108, 115, 124, 137, 137, 145]

melhorCorte = calculaMelhorCorte(n, precosBarra)

print(f"Melhor preço para corte de barra de tamanho {n}: {melhorCorte[0]}")
print(f"Esquema de corte: {melhorCorte[1]}")





    
