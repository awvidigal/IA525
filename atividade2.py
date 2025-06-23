# Algoritmo otimização de corte para barra de tamanho n
# Resolver para o caso base n=2
# Resolver para o caso base n=3 onde a melhor solução será n=2 + n=1 ou n=3
# Resolver para o caso base n=4 onde a melhor solução será n=3 + n=1 ou n=4

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
    if n == 0:
        raise ValueError("Tamanho da barra não pode nulo.")
    
    if len(precos) == 0 or len(precos) < n:
        raise ValueError("A lista de preços deve conter pelo menos n elementos.")
    
    melhorPreco = 0
    esquemaDeCorte = []

    if n == 1:
        # Caso base: barra de tamanho 1
        melhorPreco = n*precos[n-1]
        esquemaDeCorte = [1]
        return melhorPreco, esquemaDeCorte
    
    else:
        casoAnterior = calculaMelhorCorte(n-1, precos)
        barraTotal = [precos[n-1], n]

        if casoAnterior[0] + precos[0] > barraTotal[0]:
            melhorPreco = casoAnterior[0] + precos[0]
            esquemaDeCorte = casoAnterior[1] + [1]

        else:
            melhorPreco = barraTotal[0]
            esquemaDeCorte = [barraTotal[1]]
        
        return melhorPreco, esquemaDeCorte
    
n = 9
precosBarra = [0, 8, 13, 15, 12, 12, 21, 2, 18]

melhorCorte = calculaMelhorCorte(n, precosBarra)

print(f"Melhor preço para corte de barra de tamanho {n}: {melhorCorte[0]}")
print(f"Esquema de corte: {melhorCorte[1]}")





    
