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
    # Garante que o tamanho da lista de preços é pelo menos n
    if len(precos) < n:
        raise ValueError("A lista de preços deve conter pelo menos n elementos.")
    
    # Inicializa variáveis para armazenar o melhor preço e o esquema de corte
    melhorPreco = 0
    melhorEsquema = []

    # Inicializa o dicionário se não for fornecido
    if memo is None:
        memo = {}
    
    # Verifica se o resultado já foi calculado, retornando o valor memorizado se existir
    if n in memo:
        return memo[n]
    
    # Caso base: se n for 0, não há corte a ser feito
    if n == 0:
        melhorPreco = 0
        melhorEsquema = []
        return melhorPreco, melhorEsquema
    
    # Caso base: se n for 1, o melhor corte é o preço do primeiro elemento
    else:
        # Começa a calcular o melhor corte dentre todos os possíveis, de 1 até n
        for corte in range(1, n+1):
            # Cálculo recursivo para o restante da barra
            precoAtual, esquemaAtual = calculaMelhorCorte(n-corte, precos, memo)
            # Adiciona o preço do corte atual
            precoAtual += precos[corte-1]

            # Verifica se o preço atual é melhor que o melhor encontrado até agora
            if precoAtual > melhorPreco:
                melhorPreco = precoAtual
                melhorEsquema = esquemaAtual + [corte]

        # Armazena o resultado no dicionário
        memo[n] = (melhorPreco, melhorEsquema)
        
        # Retorna o melhor preço e o esquema de corte
        return memo[n]

n = 17
precosBarra = [1, 2, 10, 22, 25, 32, 59, 68, 79, 92, 102, 108, 115, 124, 137, 137, 145]

melhorCorte = calculaMelhorCorte(n, precosBarra)

print(f"Melhor preço para corte de barra de tamanho {n}: {melhorCorte[0]}")
print(f"Esquema de corte: {melhorCorte[1]}")





    
