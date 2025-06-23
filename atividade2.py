# Algoritmo otimização de corte para barra de tamanho n
# Para uma barra de tamanho n, calcular todos os cortes possíveis, comparando os preços obtidos
# Evitar cálculos repetidos memorizando os resultados já calculados em um dicionario com índice n e valores associados ao melhor preço e esquema de corte

def calculaMelhorCorte(n, precos, memo=None):
    '''
        Calcula o melhor corte para uma barra de tamanho n

        Parâmetros:
        -----------
        n : inteiro
            Tamanho da barra

        precos : vetor
            Lista de preços para cada tamanho de corte

        memo : dicionário
            Cache para armazenar resultados intermediários (opcional)

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

    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
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
       
        memo[n] = (melhorPreco, melhorEsquema)
        return memo[n]
    
# n = 17
# precosBarra = [1, 2, 10, 22, 25, 32, 59, 68, 79, 92, 102, 108, 115, 124, 137, 137, 145]

n = 4
precosBarra = [1, 5, 8, 9]

melhorCorte = calculaMelhorCorte(n, precosBarra)

print(f"Melhor preço para corte de barra de tamanho {n}: {melhorCorte[0]}")
print(f"Esquema de corte: {melhorCorte[1]}")





    
