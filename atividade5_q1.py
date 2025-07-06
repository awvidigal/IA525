from sklearn.model_selection    import train_test_split
from sklearn.datasets           import load_iris
from sklearn.metrics            import accuracy_score
from tabnanny                   import verbose
from cvxpy                      import Variable, Minimize, Problem, multiply, pos, sum_squares

import numpy as np

# dicionario que relaciona nome da especie ao valor no vetor y
especies = {
    'setosa' : 0,
    'versicolor' : 1,
    'virginica' : 2
}

iris = load_iris()

def encontraCoeficientesQuadradosMinimos(t, y, especie):
    yBinario = np.where(y == especies[especie], 1, -1)
    
    m = t.shape[1]
    
    t = t.T

    a = Variable(m)
    b = Variable()
    
    funcao      = yBinario - (a.T @ t) - b
    objective   = Minimize(sum_squares(funcao))
    problema    = Problem(objective)

    problema.solve()

    return a.value, b.value

def encontraCoeficientesSVM(t, y, especie):
    yBinario = np.where(y == especies[especie], 1, -1)
    
    m = t.shape[1]
    
    t = t.T

    a = Variable(m)
    b = Variable()

    funcao = pos(1 - multiply(yBinario, (a.T @ t + b)))
    objective = Minimize(sum(funcao))
    problema = Problem(objective)

    problema.solve()

    return a.value, b.value

# print(type(iris))
x = iris.data
y = iris.target

# print('\nx: ',x)
# print('\ny: ',y)

xTrain, xTest, yTrain, yTest = train_test_split(
    x, y,
    test_size= 50,
    random_state= 42,
    stratify= y
)

yTestSetosa     = np.where(yTest == especies['setosa'], 1, -1)
yTestVirginica  = np.where(yTest == especies['virginica'], 1, -1)
yTestVersicolor = np.where(yTest == especies['versicolor'], 1, -1)

yTrainSetosa     = np.where(yTrain == especies['setosa'], 1, -1)
yTrainVirginica  = np.where(yTrain == especies['virginica'], 1, -1)
yTrainVersicolor = np.where(yTrain == especies['versicolor'], 1, -1)

print('\n####################   Taxas de Erro   ####################')
print('\nQuadrados mínimos:')

# Classificador setosa -> Quadrados Mínimos
A, B = encontraCoeficientesQuadradosMinimos(xTrain, yTrain, 'setosa')
A.reshape(1, -1)
yPredSetosaQM = np.sign(xTest @ A + B)
taxaDeErroSetosaQM = (1 - accuracy_score(yTestSetosa, yPredSetosaQM)) * 100
print(f'Setosa Conjunto de teste -> {taxaDeErroSetosaQM:.2f}%')
yPredSetosaQM = np.sign(xTrain @ A + B)
taxaDeErroSetosaQM = (1 - accuracy_score(yTrainSetosa, yPredSetosaQM)) * 100
print(f'Setosa Conjunto de treino -> {taxaDeErroSetosaQM:.2f}%')

# Classificador virginica -> Quadrados Mínimos
A, B = encontraCoeficientesQuadradosMinimos(xTrain, yTrain, 'virginica')
A.reshape(1, -1)
yPredVirginicaQM = np.sign(xTest @ A + B)
taxaDeErroVirginicaQM = (1 - accuracy_score(yTestVirginica, yPredVirginicaQM)) * 100
print(f'Virginica Conjunto de Teste -> {taxaDeErroVirginicaQM:.2f}%')
yPredVirginicaQM = np.sign(xTrain @ A + B)
taxaDeErroVirginicaQM = (1 - accuracy_score(yTrainVirginica, yPredVirginicaQM)) * 100
print(f'Virginica Conjunto de Treino -> {taxaDeErroVirginicaQM:.2f}%')

# Classificador versicolor -> Quadrados Mínimos
A, B = encontraCoeficientesQuadradosMinimos(xTrain, yTrain, 'versicolor')
A.reshape(1, -1)
yPredVersicolorQM = np.sign(xTest @ A + B)
taxaDeErroVersicolorQM = (1 - accuracy_score(yTestVersicolor, yPredVersicolorQM)) * 100
print(f'Versicolor Conjunto de Teste -> {taxaDeErroVersicolorQM:.2f}%')
yPredVersicolorQM = np.sign(xTrain @ A + B)
taxaDeErroVersicolorQM = (1 - accuracy_score(yTrainVersicolor, yPredVersicolorQM)) * 100
print(f'Versicolor Conjunto de Treino -> {taxaDeErroVersicolorQM:.2f}%')


# Classificador setosa -> SVM
print('\nSVM:')
A,B = encontraCoeficientesSVM(xTrain, yTrain, 'setosa')
A.reshape(1, -1)
yPredSetosaSVM = np.sign(xTest @ A + B)
taxaDeErroSetosaSVM = (1 - accuracy_score(yTestSetosa, yPredSetosaSVM)) * 100
print(f'Setosa Conjunto de Teste -> {taxaDeErroSetosaSVM:.2f}%')
yPredSetosaSVM = np.sign(xTrain @ A + B)
taxaDeErroSetosaSVM = (1 - accuracy_score(yTrainSetosa, yPredSetosaSVM)) * 100
print(f'Setosa Conjunto de Treino -> {taxaDeErroSetosaSVM:.2f}%')

# Classificador virginica -> SVM
A,B = encontraCoeficientesSVM(xTrain, yTrain, 'virginica')
A.reshape(1, -1)
yPredvirginicaSVM = np.sign(xTest @ A + B)
taxaDeErroVirginicaSVM = (1 - accuracy_score(yTestVirginica, yPredvirginicaSVM)) * 100
print(f'Virginica Conjunto de Teste -> {taxaDeErroVirginicaSVM:.2f}%')
yPredvirginicaSVM = np.sign(xTrain @ A + B)
taxaDeErroVirginicaSVM = (1 - accuracy_score(yTrainVirginica, yPredvirginicaSVM)) * 100
print(f'Virginica Conjunto de Treino -> {taxaDeErroVirginicaSVM:.2f}%')

# Classificador versicolor -> SVM
A,B = encontraCoeficientesSVM(xTrain, yTrain, 'versicolor')
A.reshape(1, -1)
yPredVersicolorSVM = np.sign(xTest @ A + B)
taxaDeErroVersicolorSVM = (1 - accuracy_score(yTestVersicolor, yPredVersicolorSVM)) * 100
print(f'Versicolor Conjunto de Teste -> {taxaDeErroVersicolorSVM:.2f}%')
yPredVersicolorSVM = np.sign(xTrain @ A + B)
taxaDeErroVersicolorSVM = (1 - accuracy_score(yTrainVersicolor, yPredVersicolorSVM)) * 100
print(f'Versicolor Conjunto de Treino -> {taxaDeErroVersicolorSVM:.2f}%\n')

# print('\nQuadrados minimos -> Setosa:'      ,yPredSetosaQM)
# print('\nQuadrados minimos -> Virginica:'   ,yPredVirginicaQM)
# print('\nQuadrados minimos -> Versicolor:'  ,yPredVersicolorQM)

# print('\nSVM -> Setosa:'    ,yPredSetosaQM)
# print('\nSVM -> Virginica:' ,yPredVirginicaQM)
# print('\nSVM -> Versicolor:',yPredVersicolorQM)




















# # Contagem das classes no conjunto completo
# print("\nContagem de classes no dataset completo:")
# # Pega os valores únicos das classes (0, 1, 2) e suas contagens
# unique_classes, class_counts = np.unique(y, return_counts=True)

# # Itera sobre os valores únicos das classes
# for i, count in zip(unique_classes, class_counts):
#     # 'i' agora é o valor da classe (0, 1 ou 2)
#     # 'count' é a contagem dessa classe
#     print(f"  Classe {iris.target_names[i]}: {count} exemplos")

# # Contagem das classes no conjunto de treinamento
# import numpy as np
# print("\nContagem de classes no conjunto de TREINAMENTO:")
# unique, counts = np.unique(yTrain, return_counts=True)
# for i, u_count in zip(unique, counts):
#     print(f"  Classe {iris.target_names[i]}: {u_count} exemplos")

# # Contagem das classes no conjunto de teste
# print("\nContagem de classes no conjunto de TESTE:")
# unique, counts = np.unique(yTest, return_counts=True)
# for i, u_count in zip(unique, counts):
#     print(f"  Classe {iris.target_names[i]}: {u_count} exemplos")